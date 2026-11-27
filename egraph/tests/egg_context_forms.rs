// The certificate validator supplies context-local facts. Exercise the JSON process
// boundary and the egg proof actually returned to that validator.
use serde_json::{json, Value};
use std::io::Write;
use std::process::{Command, Output, Stdio};

fn request() -> Value {
    json!({
        "context_id": "length_equal_four",
        "targets": [
            {"id": "left", "compact": "(or carry (and p q))", "event_context": "length_equal_four"},
            {"id": "right", "compact": "(or carry q)", "event_context": "length_equal_four"}
        ],
        "pattern_rules": [
            {"name": "and-idem", "left": "(and ?a ?a)", "right": "?a"}
        ],
        "ground_rules": [
            {"name": "local-comparison", "left": "p", "right": "q",
             "event_context": "length_equal_four", "proof_status": "unsat"}
        ]
    })
}

fn invoke_bytes(data: &[u8]) -> Output {
    let mut child = Command::new(env!("CARGO_BIN_EXE_egg_context_forms"))
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    child.stdin.as_mut().unwrap().write_all(data).unwrap();
    child.wait_with_output().unwrap()
}

fn invoke(data: &Value) -> Output {
    invoke_bytes(&serde_json::to_vec(data).unwrap())
}

fn graph(data: &Value) -> Value {
    let result = invoke(data);
    assert!(
        result.status.success(),
        "{}",
        String::from_utf8_lossy(&result.stderr)
    );
    let graph: Value = serde_json::from_slice(&result.stdout).unwrap();
    assert_eq!(graph["context_id"], data["context_id"]);
    assert_eq!(
        graph["ground_rule_count"],
        data["ground_rules"].as_array().unwrap().len()
    );
    assert_eq!(
        graph["pattern_rule_count"],
        data["pattern_rules"].as_array().unwrap().len()
    );
    assert_eq!(graph["targets"].as_array().unwrap().len(), 2);
    for i in 0..2 {
        assert_eq!(graph["targets"][i]["id"], data["targets"][i]["id"]);
        assert!(graph["targets"][i]["eclass"].is_u64());
        assert!(graph["targets"][i]["eclass_before"].is_u64());
    }
    graph
}

fn proof(result: &Value) -> &str {
    let targets = &result["targets"];
    assert_ne!(targets[0]["eclass_before"], targets[1]["eclass_before"]);
    assert_eq!(targets[0]["eclass"], targets[1]["eclass"]);
    let edges = result["rewrite_explanations"].as_array().unwrap();
    assert_eq!(edges.len(), 1);
    assert_eq!(edges[0]["left"], targets[0]["id"]);
    assert_eq!(edges[0]["right"], targets[1]["id"]);
    edges[0]["explanation"].as_str().unwrap()
}

#[test]
fn a_local_leaf_fact_and_a_generic_rule_both_occur_in_the_proof() {
    let mut input = request();
    let result = graph(&input);
    assert_eq!(result["stop_reason"], "Some(Other(\"TargetsMerged\"))");
    let flat = proof(&result);
    assert_eq!(flat.lines().next(), input["targets"][0]["compact"].as_str());
    assert!(flat.contains(" local-comparison "));
    assert!(flat.contains(" and-idem "));

    for inventory in ["ground_rules", "pattern_rules"] {
        let mut missing = input.clone();
        missing[inventory] = json!([]);
        let result = graph(&missing);
        assert_eq!(result["stop_reason"], "Some(Saturated)");
        assert_ne!(
            result["targets"][0]["eclass"],
            result["targets"][1]["eclass"]
        );
        assert_eq!(result["rewrite_explanations"], json!([]));
    }

    // Reverse endpoint order without changing their IDs or scope.
    input["targets"].as_array_mut().unwrap().reverse();
    let reversed = graph(&input);
    assert_eq!(
        proof(&reversed).lines().next(),
        input["targets"][0]["compact"].as_str()
    );
}

#[test]
fn identical_targets_stop_without_a_rewrite_edge() {
    let mut input = request();
    input["targets"][1]["compact"] = input["targets"][0]["compact"].clone();
    let result = graph(&input);
    assert_eq!(result["stop_reason"], "Some(Other(\"TargetsMerged\"))");
    assert_eq!(
        result["targets"][0]["eclass_before"],
        result["targets"][1]["eclass_before"]
    );
    assert_eq!(
        result["targets"][0]["eclass"],
        result["targets"][1]["eclass"]
    );
    assert_eq!(result["rewrite_explanations"], json!([]));
}

#[test]
fn signed_alias_and_boolean_constants_are_valid_local_facts() {
    for rhs in ["(not q)", "true", "false"] {
        let mut input = request();
        input["targets"][0]["compact"] = json!("(or p q)");
        input["targets"][1]["compact"] = json!(format!("(or {rhs} q)"));
        input["ground_rules"][0]["right"] = json!(rhs);
        input["pattern_rules"] = json!([]);
        let result = graph(&input);
        assert!(proof(&result).contains(" local-comparison "), "{rhs}");
    }
}

#[test]
fn rejects_scope_identity_inventory_and_ground_shape_errors() {
    let invalid = [
        ("/context_id", json!("other")),
        ("/targets/0/event_context", json!("other")),
        ("/targets/0/id", json!("right")),
        ("/targets/1/id", json!("third")),
        ("/targets/0/compact", json!("(and p q) trailing")),
        ("/pattern_rules/0/name", json!("local-comparison")),
        ("/ground_rules/0/name", json!("invalid name")),
        ("/ground_rules/0/event_context", json!("other")),
        ("/ground_rules/0/proof_status", json!("sat")),
        ("/ground_rules/0/left", json!("(and p q)")),
        ("/ground_rules/0/left", json!("(not p)")),
        ("/ground_rules/0/left", json!("true")),
        ("/ground_rules/0/left", json!("?x")),
        ("/ground_rules/0/right", json!("(not (not q))")),
        ("/ground_rules/0/right", json!("(not true)")),
        ("/ground_rules/0/right", json!("(or q carry)")),
        ("/ground_rules/0/right", json!("q false")),
        ("/ground_rules/0/right", json!("?q")),
    ];
    for (path, replacement) in invalid {
        let mut input = request();
        *input.pointer_mut(path).unwrap() = replacement.clone();
        let result = invoke(&input);
        assert!(!result.status.success(), "accepted {path} = {replacement}");
        assert!(result.stdout.is_empty(), "malformed input emitted a graph");
    }
    for field in ["/ground_rules/0", "/pattern_rules/0", "/targets/0", ""] {
        let mut input = request();
        input.pointer_mut(field).unwrap()["unrecognized_field"] = json!("injected");
        assert!(
            !invoke(&input).status.success(),
            "accepted extra field on {field}"
        );
    }
}

#[test]
fn duplicate_keys_are_rejected_before_serde_can_replace_them() {
    let clean = serde_json::to_string(&request()).unwrap();
    for (original, overwritten) in [
        (
            r#""context_id":"length_equal_four""#,
            r#""context_id":"bogus","context_id":"length_equal_four""#,
        ),
        (
            r#""proof_status":"unsat""#,
            r#""proof_status":"sat","proof_\u0073tatus":"unsat""#,
        ),
    ] {
        assert!(clean.contains(original));
        let raw = clean.replacen(original, overwritten, 1);
        let result = invoke_bytes(raw.as_bytes());
        assert!(
            !result.status.success(),
            "accepted duplicate key: {original}"
        );
        assert!(result.stdout.is_empty());
    }
}
