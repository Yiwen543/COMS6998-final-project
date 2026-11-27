//! Check Boolean equivalence inside one explicit context, using named certified primitive equalities.
use egg::{define_language, Id, Pattern, RecExpr, Rewrite, Runner, Symbol};
use serde_json::{json, Value};
use std::{
    collections::BTreeSet,
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
        &["context_id", "targets", "pattern_rules", "ground_rules"],
    )?;
    let context = string(input, "context_id")?;
    if context.trim().is_empty() {
        return Err("empty context ID".into());
    }
    let targets = input["targets"]
        .as_array()
        .ok_or("expected targets array")?;
    if targets.len() != 2 {
        return Err("expected left and right target".into());
    }
    let mut ids = Vec::with_capacity(2);
    let mut expressions = Vec::with_capacity(2);
    for target in targets {
        fields(target, &["id", "compact", "event_context"])?;
        let id = string(target, "id")?;
        if !matches!(id, "left" | "right") || ids.contains(&id) {
            return Err(format!("unexpected or repeated target ID {id:?}").into());
        }
        if string(target, "event_context")? != context {
            return Err("target is outside the active context".into());
        }
        ids.push(id);
        expressions.push(expression(target, "compact", false)?.parse::<RecExpr<Bool>>()?);
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
        .with_time_limit(Duration::from_secs(5))
        .with_expr(&expressions[0])
        .with_expr(&expressions[1]);
    runner.egraph.rebuild();
    let roots = [runner.roots[0], runner.roots[1]];
    let before = roots.map(|r| usize::from(runner.egraph.find(r)));
    runner = runner
        .with_hook(move |r| {
            if r.egraph.find(roots[0]) == r.egraph.find(roots[1]) {
                Err("TargetsMerged".into())
            } else {
                Ok(())
            }
        })
        .run(&rules);
    let after = roots.map(|r| usize::from(runner.egraph.find(r)));
    let rows: Vec<_> = (0..2)
        .map(|i| json!({"id":ids[i],"eclass_before":before[i],"eclass":after[i]}))
        .collect();
    let mut edges = Vec::new();
    if before[0] != before[1] && after[0] == after[1] {
        // A limit can stop immediately after the merging iteration, before the next hook.
        let explanation = runner
            .explain_equivalence(&expressions[0], &expressions[1])
            .get_flat_string();
        edges.push(json!({"left":ids[0],"right":ids[1],"explanation":explanation}));
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
            eprintln!("egg_context_forms: {e}");
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
            "pattern_rules":[],"ground_rules":[{"name":"sample-zero","left":"a","right":"false",
                                               "event_context":"ctx","proof_status":"unsat"}]});
        let graph = prove(&p, 1).unwrap();
        assert_eq!(graph["stop_reason"], "Some(IterationLimit(1))");
        assert_eq!(
            graph["rewrite_explanations"][0]["explanation"],
            "a\n(Rewrite=> sample-zero false)"
        );
    }
}
