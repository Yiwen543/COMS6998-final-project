use egg::{define_language, rewrite, AstSize, Extractor, Id, Language, RecExpr, Runner, Symbol};
use serde_json::{json, Value};
use std::{io::{self, Read}, time::Duration};

define_language! {
    enum Bool {
        "true" = True,
        "false" = False,
        "not" = Not(Id),
        "and" = And([Id; 2]),
        "or" = Or([Id; 2]),
        Var(Symbol),
    }
}
fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let targets: Vec<Value> = serde_json::from_str(&input).expect("expected JSON array");
    let rules = vec![
        rewrite!("and-comm"; "(and ?a ?b)" => "(and ?b ?a)"),
        rewrite!("and-assoc"; "(and (and ?a ?b) ?c)" => "(and ?a (and ?b ?c))"),
        rewrite!("and-idem"; "(and ?a ?a)" => "?a"),
        rewrite!("and-identity"; "(and ?a true)" => "?a"),
        rewrite!("and-zero"; "(and ?a false)" => "false"),
        rewrite!("and-absorb"; "(and ?a (or ?a ?b))" => "?a"),
        rewrite!("and-distribute"; "(and ?a (or ?b ?c))" => "(or (and ?a ?b) (and ?a ?c))"),
        rewrite!("or-comm"; "(or ?a ?b)" => "(or ?b ?a)"),
        rewrite!("or-assoc"; "(or (or ?a ?b) ?c)" => "(or ?a (or ?b ?c))"),
        rewrite!("or-idem"; "(or ?a ?a)" => "?a"),
        rewrite!("or-identity"; "(or ?a false)" => "?a"),
        rewrite!("or-zero"; "(or ?a true)" => "true"),
        rewrite!("or-absorb"; "(or ?a (and ?a ?b))" => "?a"),
        rewrite!("or-distribute"; "(or ?a (and ?b ?c))" => "(and (or ?a ?b) (or ?a ?c))"),
        rewrite!("de-morgan-or"; "(not (or ?a ?b))" => "(and (not ?a) (not ?b))"),
        rewrite!("de-morgan-and"; "(not (and ?a ?b))" => "(or (not ?a) (not ?b))"),
        rewrite!("double-not"; "(not (not ?a))" => "?a"),
        rewrite!("and-true"; "(and ?a true)" => "?a"),
        rewrite!("and-true-left"; "(and true ?a)" => "?a"),
        rewrite!("not-false"; "(not false)" => "true"),
    ];
    let mut runner = Runner::<Bool, ()>::default()
        .with_iter_limit(20).with_node_limit(20000).with_time_limit(Duration::from_secs(5));
    for t in &targets {
        for key in ["compact", "expanded"] {
            let expr: RecExpr<Bool> = t[key].as_str().unwrap().parse().expect("invalid predicate");
            runner = runner.with_expr(&expr);
        }
    }
    runner = runner.run(&rules);
    let extractor = Extractor::new(&runner.egraph, AstSize);
    let mut normalized = Vec::new();
    for (i, t) in targets.iter().enumerate() {
        let a = runner.egraph.find(runner.roots[2*i]);
        let b = runner.egraph.find(runner.roots[2*i+1]);
        assert_eq!(a, b, "forms did not normalize to the same E-class: {}", t["id"]);
        let (_, best) = extractor.find_best(a);
        normalized.push(json!({"id":t["id"], "eclass":usize::from(a),
            "equivalent":true, "representative":best.to_string()}));
    }
    let classes: Vec<Value> = runner.egraph.classes().map(|c| {
        let nodes: Vec<Value> = c.nodes.iter().map(|n| json!({
            "op":n.to_string(),
            "children":n.children().iter().map(|id| usize::from(runner.egraph.find(*id))).collect::<Vec<_>>()
        })).collect();
        json!({"id":usize::from(c.id),"nodes":nodes})
    }).collect();
    println!("{}", serde_json::to_string_pretty(&json!({
        "engine":"egg 0.11.0", "semantics":"pure two-state one-bit Boolean predicates",
        "iterations":runner.iterations.len(), "stop_reason":format!("{:?}",runner.stop_reason),
        "targets":normalized, "eclasses":classes
    })).unwrap());
}
