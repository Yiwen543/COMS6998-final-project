//! Extract a DNF from the saturated e-class of a single Boolean source.
use egg::{define_language, EGraph, Id, Pattern, RecExpr, Rewrite, Runner, StopReason, Symbol};
use serde_json::{json, Value};
use std::{
    collections::{BTreeMap, BTreeSet},
    error::Error,
    io::{self, Read},
    time::{Duration, Instant},
};

define_language! {
    enum Bool {
        "true" = True, "false" = False, "not" = Not(Id),
        "and" = And([Id; 2]), "or" = Or([Id; 2]), Atom(Symbol),
    }
}

const NODE_LIMIT: usize = 20_000;
const TIME_LIMIT: Duration = Duration::from_secs(5);
const DEPTH_LIMIT: usize = 256;

// The ordering of Cost is the objective; Choice resolves ties deterministically.
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
struct Cost {
    clauses: u64,
    literals: u64,
    nodes: u64,
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
enum Choice {
    Atom(Bool),
    NegatedAtom(Bool),
    And(Id, Id),
    Or(Id, Id),
}

#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord)]
struct Pick(Cost, Choice);

#[derive(Clone, Copy)]
enum State {
    Literal,
    Clause,
    Dnf,
}

type Table = BTreeMap<Id, [Option<Pick>; 3]>;

fn pick_for(node: &Bool, graph: &EGraph<Bool, ()>, table: &Table) -> Option<(State, Pick)> {
    let literal = |choice, nodes| {
        (
            State::Literal,
            Pick(
                Cost {
                    clauses: 1,
                    literals: 1,
                    nodes,
                },
                choice,
            ),
        )
    };
    match node {
        Bool::Atom(_) | Bool::True | Bool::False => Some(literal(Choice::Atom(node.clone()), 1)),
        Bool::Not(id) => {
            // A negative literal must contain a positive atom even if that
            // child's e-class also admits compound or negative expressions.
            let atom = graph[*id].leaves().min()?;
            Some(literal(Choice::NegatedAtom(atom.clone()), 2))
        }
        Bool::And([left, right]) | Bool::Or([left, right]) => {
            let left = graph.find(*left);
            let right = graph.find(*right);
            let (state, choice) = match node {
                Bool::And(_) => (State::Clause, Choice::And(left, right)),
                _ => (State::Dnf, Choice::Or(left, right)),
            };
            let a = table.get(&left)?[state as usize].as_ref()?.0;
            let b = table.get(&right)?[state as usize].as_ref()?.0;
            let cost = Cost {
                clauses: if matches!(state, State::Clause) {
                    1
                } else {
                    a.clauses.saturating_add(b.clauses)
                },
                literals: a.literals.saturating_add(b.literals),
                nodes: a.nodes.saturating_add(b.nodes).saturating_add(1),
            };
            Some((state, Pick(cost, choice)))
        }
    }
}

fn dnf_choices(graph: &EGraph<Bool, ()>) -> Result<Table, &'static str> {
    let deadline = Instant::now() + TIME_LIMIT;
    let mut pending: BTreeSet<_> = graph.classes().map(|c| c.id).collect();
    let mut table = Table::new();
    while let Some(id) = pending.pop_first() {
        if Instant::now() >= deadline {
            return Err("Some(ExtractionTimeLimit)");
        }
        let mut best = table.get(&id).cloned().unwrap_or_default();
        for node in &graph[id].nodes {
            if let Some((state, candidate)) = pick_for(node, graph, &table) {
                // Every literal also satisfies Clause and Dnf; every clause satisfies Dnf.
                for previous in &mut best[state as usize..] {
                    if previous.as_ref().is_none_or(|old| &candidate < old) {
                        *previous = Some(candidate.clone());
                    }
                }
            }
        }
        if table.get(&id) != Some(&best) {
            table.insert(id, best);
            pending.extend(graph[id].parents().map(|parent| graph.find(parent)));
        }
    }
    Ok(table)
}

fn build_expr(
    table: &Table,
    id: Id,
    state: State,
    expr: &mut RecExpr<Bool>,
    depth: usize,
) -> Result<Id, &'static str> {
    if depth > DEPTH_LIMIT {
        return Err("Some(ExtractionDepthLimit)");
    }
    let node = match &table[&id][state as usize]
        .as_ref()
        .expect("missing grammar derivation")
        .1
    {
        Choice::Atom(atom) => atom.clone(),
        Choice::NegatedAtom(atom) => Bool::Not(expr.add(atom.clone())),
        Choice::And(l, r) => Bool::And([
            build_expr(table, *l, State::Clause, expr, depth + 1)?,
            build_expr(table, *r, State::Clause, expr, depth + 1)?,
        ]),
        Choice::Or(l, r) => Bool::Or([
            build_expr(table, *l, State::Dnf, expr, depth + 1)?,
            build_expr(table, *r, State::Dnf, expr, depth + 1)?,
        ]),
    };
    Ok(expr.add(node))
}

fn extract(
    graph: &EGraph<Bool, ()>,
    root: Id,
) -> Result<Option<(RecExpr<Bool>, Cost)>, &'static str> {
    let table = dnf_choices(graph)?;
    let Some(pick) = table[&root][State::Dnf as usize].as_ref() else {
        return Ok(None);
    };
    if pick.0.nodes > NODE_LIMIT as u64 {
        return Err("Some(ExtractionNodeLimit)");
    }
    let mut term = RecExpr::default();
    build_expr(&table, root, State::Dnf, &mut term, 0)?;
    Ok(Some((term, pick.0)))
}

fn token<'a>(rest: &mut &'a str) -> Result<&'a str, String> {
    *rest = rest.trim_start();
    let len = rest
        .find(|c: char| c.is_whitespace() || c == '(' || c == ')')
        .unwrap_or(rest.len());
    let (name, suffix) = rest.split_at(len);
    if name.is_empty() || name.contains(['"', '\\']) {
        return Err("expected an unquoted Boolean token".into());
    }
    *rest = suffix;
    Ok(name)
}

fn check_syntax(rest: &mut &str, depth: usize, pattern: bool) -> Result<(), String> {
    if depth > DEPTH_LIMIT {
        return Err("expression exceeds supported nesting depth".into());
    }
    *rest = rest.trim_start();
    if let Some(tail) = rest.strip_prefix('(') {
        *rest = tail;
        let arity = match token(rest)? {
            "not" => 1,
            "and" | "or" => 2,
            _ => return Err("unknown Boolean operator".into()),
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
        if matches!(name, "not" | "and" | "or") || name.starts_with("Rewrite") {
            return Err(format!("reserved atom {name:?}"));
        }
        if let Some(var) = name.strip_prefix('?') {
            let mut letters = var.bytes();
            if !pattern
                || !letters
                    .next()
                    .is_some_and(|c| c.is_ascii_alphabetic() || c == b'_')
                || !letters.all(|c| c.is_ascii_alphanumeric() || c == b'_')
            {
                return Err(format!("invalid variable {name:?}"));
            }
        }
    }
    Ok(())
}

fn expression_text<'a>(value: &'a Value, field: &str) -> Result<&'a str, String> {
    let text = value[field]
        .as_str()
        .ok_or_else(|| format!("expected string {field}"))?;
    let mut rest = text;
    check_syntax(&mut rest, 0, field != "term")?;
    if !rest.trim().is_empty() {
        return Err("unexpected trailing expression tokens".into());
    }
    Ok(text)
}

fn run(payload: &Value) -> Result<Value, Box<dyn Error>> {
    let fields = payload.as_object().ok_or("expected a JSON object")?;
    if fields.len() != 2 || !fields.contains_key("term") || !fields.contains_key("pattern_rules") {
        return Err("expected only term and pattern_rules".into());
    }
    let source_text = expression_text(payload, "term")?;
    let source: RecExpr<Bool> = source_text.parse()?;
    let mut rules = Vec::new();
    let mut names = BTreeSet::new();
    for rule in payload["pattern_rules"]
        .as_array()
        .ok_or("expected pattern_rules array")?
    {
        let name = rule["name"].as_str().ok_or("expected rule name")?;
        if name.is_empty()
            || name.contains(['(', ')'])
            || name.chars().any(char::is_whitespace)
            || !names.insert(name)
        {
            return Err(format!("invalid or duplicate rule name {name:?}").into());
        }
        let lhs: Pattern<Bool> = expression_text(rule, "left")?.parse()?;
        let rhs: Pattern<Bool> = expression_text(rule, "right")?.parse()?;
        if lhs.vars().into_iter().collect::<BTreeSet<_>>() != rhs.vars().into_iter().collect() {
            return Err(format!("different variable sets in {name}").into());
        }
        rules.push(Rewrite::<Bool, ()>::new(name, lhs, rhs)?);
    }

    let mut runner = Runner::<Bool, ()>::default()
        .with_explanations_enabled()
        .with_iter_limit(20)
        .with_node_limit(NODE_LIMIT)
        .with_time_limit(TIME_LIMIT)
        .with_expr(&source)
        .run(&rules);
    let mut output = json!({
        "source":source_text,"extracted":null,"explanation":null,"clause_count":null,"literal_count":null,
        "stop_reason":format!("{:?}",runner.stop_reason),"iterations":runner.iterations.len(),
        "eclasses":runner.egraph.number_of_classes(),"enodes":runner.egraph.total_size()
    });
    if matches!(runner.stop_reason, Some(StopReason::Saturated)) {
        let root = runner.egraph.find(runner.roots[0]);
        match extract(&runner.egraph, root) {
            Err(reason) => output["stop_reason"] = json!(reason),
            Ok(None) => {}
            Ok(Some((term, cost))) => {
                // lookup_expr is read-only. Check that the entire chosen tree is
                // represented before asking egg to materialize its flat proof.
                if runner.egraph.lookup_expr(&term) != Some(root) {
                    return Err("extracted DNF is absent from the saturated root".into());
                }
                let text = term.to_string();
                if text != source.to_string() {
                    output["explanation"] =
                        json!(runner.explain_equivalence(&source, &term).get_flat_string());
                }
                output["extracted"] = json!(text);
                output["clause_count"] = json!(cost.clauses);
                output["literal_count"] = json!(cost.literals);
            }
        }
    }
    Ok(output)
}

fn main() {
    let result = (|| -> Result<Value, Box<dyn Error>> {
        let mut input = String::new();
        const INPUT_LIMIT: usize = 1024 * 1024;
        io::stdin()
            .take(INPUT_LIMIT as u64 + 1)
            .read_to_string(&mut input)?;
        if input.len() > INPUT_LIMIT {
            return Err("input exceeds 1 MiB".into());
        }
        run(&serde_json::from_str(&input)?)
    })();
    match result {
        Ok(output) => println!("{output:#}"),
        Err(err) => {
            eprintln!("egg_diagnostic_forms: {err}");
            std::process::exit(1);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn factored_source_only() {
        let term = "(and a (or b c))";
        let rule = json!({"name":"distribute","left":"(and ?a (or ?b ?c))",
                          "right":"(or (and ?a ?b) (and ?a ?c))"});
        let result = run(&json!({"term":term,"pattern_rules":[rule]})).unwrap();
        assert_eq!(result["extracted"], "(or (and a b) (and a c))");
        assert_eq!(result["clause_count"], 2);
        assert_eq!(result["literal_count"], 4);
        assert!(result["explanation"]
            .as_str()
            .unwrap()
            .contains("Rewrite=> distribute"));
        let miss = run(&json!({"term":term,"pattern_rules":[]})).unwrap();
        assert_eq!(miss["stop_reason"], "Some(Saturated)");
        assert!(miss["extracted"].is_null());
        assert!(run(&json!({"term":term,"pattern_rules":[],"target":"a"})).is_err());
    }

    #[test]
    fn rejects_trailing_tokens_and_non_boolean_forms() {
        for term in [
            "(and a b) c",
            "(and and x)",
            "?unbound",
            "(not)",
            "(x)",
            "x )",
        ] {
            assert!(
                run(&json!({"term":term,"pattern_rules":[]})).is_err(),
                "{term:?}"
            );
        }
    }

    #[test]
    fn minimizes_clauses_then_literals() {
        let source = "(or (and a (and b b)) (and a (and b b)))";
        let result = run(&json!({"term":source,"pattern_rules":[
            {"name":"or-idem","left":"(or ?x ?x)","right":"?x"},
            {"name":"and-idem","left":"(and ?x ?x)","right":"?x"}
        ]}))
        .unwrap();
        assert_eq!(result["extracted"], "(and a b)");
        assert_eq!(result["clause_count"], 1);
        assert_eq!(result["literal_count"], 2);
        let negated = run(&json!({"term":"(not (not a))","pattern_rules":[]})).unwrap();
        assert!(negated["extracted"].is_null());
    }
}
