//! Multi-target Boolean equivalence inside ONE explicit context, using named certified primitive equalities.
//! The caller owns typed fact certification and context partitioning; this executable only searches for derivations.
use egg::{define_language, Id, Pattern, RecExpr, Rewrite, Runner, Symbol};
use serde_json::{json, Value};
use std::{
    collections::{BTreeMap, BTreeSet},
    error::Error,
    io::{self, Read},
    time::Duration,
};

define_language! {
    enum Bool {
        "true" = True, "false" = False, "not" = Not(Id),
        "and" = And([Id; 2]), "or" = Or([Id; 2]), Atom(Symbol),
    }
}

const INPUT_LIMIT: usize = 1024 * 1024;

fn string<'a>(value: &'a Value, key: &str) -> Result<&'a str, String> {
    value[key]
        .as_str()
        .ok_or_else(|| format!("expected string field {key}"))
}

fn fields(value: &Value, expected: &[&str]) -> Result<(), String> {
    let object = value.as_object().ok_or("expected a JSON object")?;
    if object.len() != expected.len() || !expected.iter().all(|k| object.contains_key(*k)) {
        return Err(format!("expected exactly the fields {expected:?}"));
    }
    Ok(())
}

fn read_json(input: &str) -> Result<Value, Box<dyn Error>> {
    let value: Value = serde_json::from_str(input)?;
    // A colon outside strings in valid JSON denotes exactly one object member.
    // Value keeps the last duplicate. Compare the parsed count to the wire count,
    // including semantic duplicate keys with different JSON escape spellings.
    fn members(v: &Value) -> usize {
        match v {
            Value::Object(m) => m.len() + m.values().map(members).sum::<usize>(),
            Value::Array(a) => a.iter().map(members).sum(),
            _ => 0,
        }
    }
    let (mut quoted, mut escaped, mut count) = (false, false, 0);
    for b in input.bytes() {
        if escaped {
            escaped = false;
        } else if b == b'\\' && quoted {
            escaped = true;
        } else if b == b'"' {
            quoted = !quoted;
        } else if b == b':' && !quoted {
            count += 1;
        }
    }
    if count != members(&value) {
        return Err("duplicate JSON object member".into());
    }
    Ok(value)
}

fn identifier(text: &str) -> bool {
    let mut chars = text.bytes();
    chars
        .next()
        .is_some_and(|b| b.is_ascii_alphabetic() || b == b'_')
        && chars.all(|b| b.is_ascii_alphanumeric() || b == b'_')
}

fn token<'a>(input: &mut &'a str) -> Result<&'a str, String> {
    *input = input.trim_start();
    let length = input
        .find(|c: char| c == '(' || c == ')' || c.is_whitespace())
        .unwrap_or(input.len());
    if length == 0 {
        return Err("expected Boolean token".into());
    }
    let (first, rest) = input.split_at(length);
    *input = rest;
    Ok(first)
}

fn expression<'a>(value: &'a Value, key: &str, pattern: bool) -> Result<&'a str, String> {
    fn check(input: &mut &str, pattern: bool, depth: usize) -> Result<(), String> {
        if depth > 256 {
            return Err("expression exceeds supported nesting depth".into());
        }
        *input = input.trim_start();
        if let Some(rest) = input.strip_prefix('(') {
            *input = rest;
            let arity = match token(input)? {
                "not" => 1,
                "and" | "or" => 2,
                op => return Err(format!("unknown Boolean operator {op:?}")),
            };
            for _ in 0..arity {
                check(input, pattern, depth + 1)?;
            }
            *input = input
                .trim_start()
                .strip_prefix(')')
                .ok_or("incorrect Boolean arity")?;
        } else {
            let name = token(input)?;
            let valid = if matches!(name, "true" | "false") {
                true
            } else if pattern {
                // Generic schemas may use variables and constants, never named DUT atoms.
                name.strip_prefix('?').is_some_and(identifier)
            } else {
                identifier(name)
                    && !matches!(name, "not" | "and" | "or")
                    && !name.starts_with("Rewrite")
            };
            if !valid {
                return Err(format!("invalid Boolean leaf {name:?}"));
            }
        }
        Ok(())
    }
    let text = string(value, key)?;
    let mut remainder = text;
    check(&mut remainder, pattern, 0)?;
    if !remainder.trim().is_empty() {
        return Err("unexpected trailing expression tokens".into());
    }
    Ok(text)
}

fn add_name<'a>(row: &'a Value, names: &mut BTreeSet<&'a str>) -> Result<&'a str, String> {
    let name = string(row, "name")?;
    if name.is_empty()
        || !name
            .bytes()
            .all(|b| b.is_ascii_alphanumeric() || matches!(b, b'_' | b'-'))
        || !names.insert(name)
    {
        return Err(format!("invalid or duplicate rewrite name {name:?}"));
    }
    Ok(name)
}

fn prove(input: &Value, iter_limit: usize) -> Result<Value, Box<dyn Error>> {
    fields(
        input,
        &[
            "context_id",
            "targets",
            "pattern_rules",
            "ground_rules",
            "pairs",
        ],
    )?;
    let context = string(input, "context_id")?;
    if context.trim().is_empty() {
        return Err("empty context ID".into());
    }
    let targets = input["targets"]
        .as_array()
        .ok_or("expected targets array")?;
    if targets.len() < 2 {
        return Err("expected at least two targets".into());
    }
    let mut ids = Vec::with_capacity(targets.len());
    let mut index = BTreeMap::new();
    let mut expressions = Vec::with_capacity(targets.len());
    for target in targets {
        fields(target, &["id", "compact", "event_context"])?;
        let id = string(target, "id")?;
        if id.trim().is_empty() || index.insert(id, ids.len()).is_some() {
            return Err(format!("unexpected or repeated target ID {id:?}").into());
        }
        if string(target, "event_context")? != context {
            return Err("target is outside the active context".into());
        }
        ids.push(id);
        expressions.push(expression(target, "compact", false)?.parse::<RecExpr<Bool>>()?);
    }
    let pair_rows = input["pairs"].as_array().ok_or("expected pairs array")?;
    if pair_rows.is_empty() {
        return Err("at least one pair is required".into());
    }
    let mut pairs = Vec::with_capacity(pair_rows.len());
    let mut seen_pairs = BTreeSet::new();
    for pair in pair_rows {
        let pair = pair.as_array().ok_or("expected pair list")?;
        if pair.len() != 2 {
            return Err("pair requires exactly two IDs".into());
        }
        let a = *index
            .get(pair[0].as_str().ok_or("pair ID must be a string")?)
            .ok_or("unknown first pair ID")?;
        let b = *index
            .get(pair[1].as_str().ok_or("pair ID must be a string")?)
            .ok_or("unknown second pair ID")?;
        if a == b || !seen_pairs.insert((a.min(b), a.max(b))) {
            return Err("self-pair or duplicated unordered pair".into());
        }
        pairs.push((a, b));
    }
    let patterns = input["pattern_rules"]
        .as_array()
        .ok_or("expected pattern rules array")?;
    let ground = input["ground_rules"]
        .as_array()
        .ok_or("expected ground rules array")?;
    let mut rules = Vec::with_capacity(patterns.len() + ground.len());
    let mut names = BTreeSet::new();
    for row in patterns {
        fields(row, &["name", "left", "right"])?;
        let name = add_name(row, &mut names)?;
        let left: Pattern<Bool> = expression(row, "left", true)?.parse()?;
        let right: Pattern<Bool> = expression(row, "right", true)?.parse()?;
        let vars: BTreeSet<_> = left.vars().into_iter().collect();
        if right.vars().iter().any(|v| !vars.contains(v)) {
            return Err(format!("unbound RHS variable in {name}").into());
        }
        rules.push(Rewrite::<Bool, ()>::new(name, left, right)?);
    }
    for row in ground {
        fields(
            row,
            &["name", "left", "right", "event_context", "proof_status"],
        )?;
        let name = add_name(row, &mut names)?;
        if string(row, "event_context")? != context || string(row, "proof_status")? != "unsat" {
            return Err("ground equality needs an UNSAT certificate in this context".into());
        }
        let left_text = expression(row, "left", false)?;
        let right_text = expression(row, "right", false)?;
        let left: RecExpr<Bool> = left_text.parse()?;
        let right: RecExpr<Bool> = right_text.parse()?;
        if !matches!(left.as_ref(), [Bool::Atom(_)])
            || !matches!(
                right.as_ref(),
                [Bool::Atom(_) | Bool::True | Bool::False] | [Bool::Atom(_), Bool::Not(_)]
            )
        {
            return Err("ground equality must bind a primitive to a literal, constant or complemented primitive".into());
        }
        // These are ordinary named ground rewrites, not direct e-class unions.
        rules.push(Rewrite::<Bool, ()>::new(
            name,
            left_text.parse::<Pattern<Bool>>()?,
            right_text.parse::<Pattern<Bool>>()?,
        )?);
    }

    let mut runner = Runner::<Bool, ()>::default()
        .with_explanations_enabled()
        .with_iter_limit(iter_limit)
        .with_node_limit(20_000)
        .with_time_limit(Duration::from_secs(5));
    for expression in &expressions {
        runner = runner.with_expr(expression);
    }
    runner.egraph.rebuild();
    let roots = runner.roots.clone();
    let before: Vec<_> = roots
        .iter()
        .map(|&r| usize::from(runner.egraph.find(r)))
        .collect();
    let hook_roots = roots.clone();
    let hook_pairs = pairs.clone();
    runner = runner
        .with_hook(move |r| {
            if hook_pairs
                .iter()
                .all(|&(a, b)| r.egraph.find(hook_roots[a]) == r.egraph.find(hook_roots[b]))
            {
                Err("TargetsMerged".into())
            } else {
                Ok(())
            }
        })
        .run(&rules);
    let after: Vec<_> = roots
        .iter()
        .map(|&r| usize::from(runner.egraph.find(r)))
        .collect();
    let rows: Vec<_> = (0..ids.len())
        .map(|i| json!({"id":ids[i],"eclass_before":before[i],"eclass":after[i]}))
        .collect();
    // Never present an unrequested e-class collision as a proved obligation.
    // Preserve checked explanations even when another requested target never merges.
    let mut edges = Vec::new();
    for (a, b) in pairs {
        if before[a] != before[b] && after[a] == after[b] {
            let explanation = runner
                .explain_equivalence(&expressions[a], &expressions[b])
                .get_flat_string();
            edges.push(json!({"left":ids[a],"right":ids[b],"explanation":explanation}));
        }
    }
    Ok(json!({
        "engine":"egg 0.11.0", "context_id":context, "stop_reason":format!("{:?}",runner.stop_reason),
        "iterations":runner.iterations.len(), "enodes":runner.egraph.total_size(), "eclasses":runner.egraph.number_of_classes(),
        "pattern_rule_count":patterns.len(), "ground_rule_count":ground.len(),"targets":rows,"rewrite_explanations":edges
    }))
}

fn main() {
    let result = (|| -> Result<Value, Box<dyn Error>> {
        let mut input = String::new();
        io::stdin()
            .take(INPUT_LIMIT as u64 + 1)
            .read_to_string(&mut input)?;
        if input.len() > INPUT_LIMIT {
            return Err("input exceeds 1 MiB".into());
        }
        prove(&read_json(&input)?, 20)
    })();
    match result {
        Ok(graph) => println!("{graph}"),
        Err(e) => {
            eprintln!("egg_regression_forms: {e}");
            std::process::exit(1);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn retains_proof_when_stop_coincides_with_merge() {
        let p = json!({"context_id":"ctx","targets":[
            {"id":"left","compact":"a","event_context":"ctx"},
            {"id":"right","compact":"false","event_context":"ctx"}],
            "pairs":[["left","right"]],"pattern_rules":[],"ground_rules":[{"name":"sample-zero","left":"a","right":"false",
                                               "event_context":"ctx","proof_status":"unsat"}]});
        let graph = prove(&p, 1).unwrap();
        assert_eq!(graph["stop_reason"], "Some(IterationLimit(1))");
        assert_eq!(
            graph["rewrite_explanations"][0]["explanation"],
            "a\n(Rewrite=> sample-zero false)"
        );
    }
}
