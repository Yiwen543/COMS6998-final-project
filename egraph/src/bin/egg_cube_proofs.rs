//! Prove a restricted Boolean term equal to true using the supplied pattern rules.
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

fn identifier(name: &str) -> bool {
    let mut bytes = name.bytes();
    bytes
        .next()
        .is_some_and(|b| b.is_ascii_alphabetic() || b == b'_')
        && bytes.all(|b| b.is_ascii_alphanumeric() || b == b'_')
}

fn token<'a>(rest: &mut &'a str) -> Result<&'a str, String> {
    *rest = rest.trim_start();
    let len = rest
        .find(|c: char| c.is_whitespace() || c == '(' || c == ')')
        .unwrap_or(rest.len());
    let (word, tail) = rest.split_at(len);
    if word.is_empty() {
        return Err("expected Boolean token".into());
    }
    *rest = tail;
    Ok(word)
}

fn check_syntax(rest: &mut &str, depth: usize, pattern: bool) -> Result<(), String> {
    if depth > 256 {
        return Err("expression exceeds supported nesting depth".into());
    }
    *rest = rest.trim_start();
    if let Some(tail) = rest.strip_prefix('(') {
        *rest = tail;
        let arity = match token(rest)? {
            "not" => 1,
            "and" | "or" => 2,
            op => return Err(format!("unknown Boolean operator {op:?}")),
        };
        for _ in 0..arity {
            check_syntax(rest, depth + 1, pattern)?;
        }
        *rest = rest
            .trim_start()
            .strip_prefix(')')
            .ok_or("wrong number of operands")?;
    } else {
        let name = token(rest)?;
        if let Some(var) = name.strip_prefix('?') {
            if !pattern || !identifier(var) {
                return Err(format!("invalid variable {name:?}"));
            }
        } else if !identifier(name)
            || matches!(name, "not" | "and" | "or")
            || name.starts_with("Rewrite")
        {
            return Err(format!("invalid Boolean atom {name:?}"));
        }
    }
    Ok(())
}

fn expression<'a>(value: &'a Value, key: &str) -> Result<&'a str, String> {
    let text = value[key]
        .as_str()
        .ok_or_else(|| format!("expected string {key}"))?;
    let mut rest = text;
    check_syntax(&mut rest, 0, key != "term")?;
    if !rest.trim().is_empty() {
        return Err("unexpected trailing expression tokens".into());
    }
    Ok(text)
}

fn fields(value: &Value, keys: &[&str]) -> Result<(), String> {
    let object = value.as_object().ok_or("expected JSON object")?;
    if object.len() != keys.len() || keys.iter().any(|&key| !object.contains_key(key)) {
        return Err(format!("expected exactly these fields: {keys:?}"));
    }
    Ok(())
}

fn prove(input: &Value, iter_limit: usize) -> Result<Value, Box<dyn Error>> {
    fields(input, &["term", "pattern_rules"])?;
    let source_text = expression(input, "term")?;
    let source: RecExpr<Bool> = source_text.parse()?;
    let target: RecExpr<Bool> = "true".parse()?;
    let mut rules = Vec::new();
    let mut names = BTreeSet::new();
    for rule in input["pattern_rules"]
        .as_array()
        .ok_or("expected pattern_rules array")?
    {
        fields(rule, &["name", "left", "right"])?;
        let name = rule["name"].as_str().ok_or("expected string rule name")?;
        if name.is_empty()
            || !name
                .bytes()
                .all(|b| b.is_ascii_alphanumeric() || matches!(b, b'_' | b'-'))
            || !names.insert(name)
        {
            return Err(format!("invalid or duplicate rule name {name:?}").into());
        }
        let lhs: Pattern<Bool> = expression(rule, "left")?.parse()?;
        let rhs: Pattern<Bool> = expression(rule, "right")?.parse()?;
        let bindings: BTreeSet<_> = lhs.vars().into_iter().collect();
        if rhs.vars().iter().any(|var| !bindings.contains(var)) {
            return Err(format!("unbound RHS variable in rule {name}").into());
        }
        rules.push(Rewrite::<Bool, ()>::new(name, lhs, rhs)?);
    }

    let mut runner = Runner::<Bool, ()>::default()
        .with_explanations_enabled()
        .with_iter_limit(iter_limit)
        .with_node_limit(20_000)
        .with_time_limit(Duration::from_secs(5))
        .with_expr(&source)
        .with_expr(&target);
    runner.egraph.rebuild();
    let (left, right) = (runner.roots[0], runner.roots[1]);
    runner = runner
        .with_hook(move |r| {
            if r.egraph.find(left) == r.egraph.find(right) {
                Err("TargetsMerged".into())
            } else {
                Ok(())
            }
        })
        .run(&rules);

    // A limit may fire after the last rewrite but before the next hook.
    let merged = runner.egraph.find(left) == runner.egraph.find(right);
    let proof = if merged && source != target {
        Some(
            runner
                .explain_equivalence(&source, &target)
                .get_flat_string(),
        )
    } else {
        None
    };
    Ok(json!({
        "source": source_text, "target": "true", "merged": merged,
        "stop_reason": format!("{:?}", runner.stop_reason), "explanation": proof,
        "iterations": runner.iterations.len(), "enodes": runner.egraph.total_size(),
        "eclasses": runner.egraph.number_of_classes()
    }))
}

fn main() {
    let result = (|| -> Result<Value, Box<dyn Error>> {
        const INPUT_LIMIT: usize = 1024 * 1024;
        let mut input = String::new();
        io::stdin()
            .take(INPUT_LIMIT as u64 + 1)
            .read_to_string(&mut input)?;
        if input.len() > INPUT_LIMIT {
            return Err("input exceeds 1 MiB".into());
        }
        prove(&serde_json::from_str(&input)?, 20)
    })();
    match result {
        Ok(out) => println!("{out}"),
        Err(err) => {
            eprintln!("egg_cube_proofs: {err}");
            std::process::exit(1);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn erasing() -> Value {
        json!({"term":"(or (not x) true)","pattern_rules":[{"name":"or-true","left":"(or ?x true)","right":"true"}]})
    }

    #[test]
    fn erases_unused_variable_with_full_proof() {
        let result = prove(&erasing(), 20).unwrap();
        assert_eq!(result["stop_reason"], "Some(Other(\"TargetsMerged\"))");
        assert_eq!(result["merged"], true);
        assert_eq!(
            result["explanation"],
            "(or (not x) true)\n(Rewrite=> or-true true)"
        );
    }

    #[test]
    fn preserves_proof_when_merge_and_limit_coincide() {
        let result = prove(&erasing(), 1).unwrap();
        assert_eq!(result["stop_reason"], "Some(IterationLimit(1))");
        assert_eq!(result["merged"], true);
        assert!(result["explanation"].is_string());
    }

    #[test]
    fn distinguishes_identity_from_unproved() {
        for (term, merged) in [("true", true), ("false", false), ("atom_0", false)] {
            let out = prove(&json!({"term":term,"pattern_rules":[]}), 20).unwrap();
            assert_eq!(out["merged"], merged);
            assert!(out["explanation"].is_null());
        }
    }

    #[test]
    fn rejects_trailing_tokens_and_malformed_terms() {
        for term in [
            "x y",
            "(not x) true",
            "(not x)(",
            "(and x)",
            "(not x y)",
            "(xor x y)",
            "?x",
            "\"x\"",
            "and",
            ")",
        ] {
            assert!(
                prove(&json!({"term":term,"pattern_rules":[]}), 20).is_err(),
                "{term}"
            );
        }
        for key in ["left", "right"] {
            let mut input = erasing();
            input["pattern_rules"][0][key] = json!("?x false");
            assert!(prove(&input, 20).is_err());
        }
    }

    #[test]
    fn rejects_unbound_variables_and_unknown_keys() {
        let mut input = erasing();
        input["pattern_rules"][0]["right"] = json!("?y");
        assert!(prove(&input, 20).is_err());
        let mut input = erasing();
        input["target"] = json!("false");
        assert!(prove(&input, 20).is_err());
        let mut input = erasing();
        input["pattern_rules"][0]["unexpected"] = json!(true);
        assert!(prove(&input, 20).is_err());
    }
}
