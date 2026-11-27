//! Compare same-scope Boolean violation formulas for a sampled RTL assertion.
//! The Python caller independently certifies the supplied patterns and proofs.
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
        "true" = True,
        "false" = False,
        "not" = Not(Id),
        "and" = And([Id; 2]),
        "or" = Or([Id; 2]),
        Atom(Symbol),
    }
}

fn field<'a>(value: &'a Value, key: &str) -> Result<&'a str, String> {
    value[key]
        .as_str()
        .ok_or_else(|| format!("expected string field {key}"))
}

fn run() -> Result<Value, Box<dyn Error>> {
    let args: Vec<_> = std::env::args().skip(1).collect();
    let stop_on_merge = match args.as_slice() {
        [] => false,
        [flag] if flag == "--stop-on-merge" => true,
        _ => return Err("usage: egg_assertion_forms [--stop-on-merge]".into()),
    };
    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;
    let payload: Value = serde_json::from_str(&input)?;
    let targets = payload["targets"].as_array().ok_or("missing targets")?;
    if payload["verified_rules"].as_array().map(Vec::len) != Some(0) {
        return Err("ground rules are outside the assertion-form engine".into());
    }
    let mut ids = BTreeSet::new();
    let mut exprs = Vec::with_capacity(targets.len());
    for target in targets {
        let id = field(target, "id")?;
        if !ids.insert(id) || target["event_context"].is_null() {
            return Err(format!("duplicate target or missing event context for {id}").into());
        }
        exprs.push(field(target, "compact")?.parse::<RecExpr<Bool>>()?);
    }
    if exprs.is_empty() {
        return Err("at least one target is required".into());
    }
    if stop_on_merge && (targets.len() != 2 || targets[0]["event_context"] != targets[1]["event_context"]) {
        return Err("--stop-on-merge requires exactly two targets in the same event context".into());
    }

    let mut names = BTreeSet::new();
    let mut rules = Vec::new();
    for rule in payload["pattern_rules"].as_array().ok_or("missing pattern rules")? {
        let name = field(rule, "name")?;
        let lhs = field(rule, "left")?.parse::<Pattern<Bool>>()?;
        let rhs = field(rule, "right")?.parse::<Pattern<Bool>>()?;
        let vars = |pattern: &Pattern<Bool>| pattern.vars().into_iter().collect::<BTreeSet<_>>();
        if !names.insert(name) || vars(&lhs) != vars(&rhs) {
            return Err(format!("duplicate or non-reversible pattern {name}").into());
        }
        rules.push(Rewrite::<Bool, ()>::new(name, lhs, rhs)?);
    }

    let mut runner = Runner::<Bool, ()>::default()
        .with_explanations_enabled()
        .with_iter_limit(20)
        .with_node_limit(20_000)
        .with_time_limit(Duration::from_secs(5));
    for expr in &exprs {
        runner = runner.with_expr(expr);
    }
    runner.egraph.rebuild();
    let roots = |runner: &Runner<Bool, ()>| {
        runner.roots.iter().map(|&id| usize::from(runner.egraph.find(id))).collect::<Vec<_>>()
    };
    let before = roots(&runner);
    if stop_on_merge {
        let (left, right) = (runner.roots[0], runner.roots[1]);
        // egg calls hooks before matching, on the rebuilt graph. This also
        // handles identical input trees before the first rewrite search.
        runner = runner.with_hook(move |r| {
            if r.egraph.find(left) == r.egraph.find(right) {
                Err("TargetsMerged".into())
            } else {
                Ok(())
            }
        });
    }
    runner = runner.run(&rules);
    let after = roots(&runner);
    let mut groups = BTreeMap::<_, Vec<_>>::new();
    let mut rows = Vec::new();
    for (i, target) in targets.iter().enumerate() {
        groups.entry((after[i], target["event_context"].to_string())).or_default().push(i);
        rows.push(json!({"id": target["id"], "eclass_before": before[i], "eclass": after[i]}));
    }

    // Connect different initial classes without requesting quadratic explanations.
    let mut explanations = Vec::new();
    for members in groups.values() {
        let first = members[0];
        if let Some(&distinct) = members.iter().find(|&&i| before[i] != before[first]) {
            for &i in members.iter().skip(1) {
                let from = if before[i] == before[first] { distinct } else { first };
                let proof = runner.explain_equivalence(&exprs[from], &exprs[i]).get_flat_string();
                explanations.push(json!({
                    "left": targets[from]["id"], "right": targets[i]["id"], "explanation": proof
                }));
            }
        }
    }
    Ok(json!({
        "engine": "egg 0.11.0",
        "stop_reason": format!("{:?}", runner.stop_reason),
        "iterations": runner.iterations.len(),
        "eclasses": runner.egraph.number_of_classes(),
        "enodes": runner.egraph.total_size(),
        "pattern_rule_count": rules.len(),
        "ground_rule_count": 0,
        "targets": rows,
        "rewrite_explanations": explanations
    }))
}

fn main() {
    match run() {
        Ok(output) => println!("{output:#}"),
        Err(err) => {
            eprintln!("egg_assertion_forms: {err}");
            std::process::exit(1);
        }
    }
}
