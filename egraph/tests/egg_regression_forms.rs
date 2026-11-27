//! Verify the multi-target process contract, not merely its class IDs.
use serde_json::{json, Value};
use std::io::Write;
use std::process::{Command, Output, Stdio};

fn request() -> Value {
    json!({
        "context_id": "ctx-A",
        "targets": [
            {"id":"P","compact":"(and p q)","event_context":"ctx-A"},
            {"id":"Q","compact":"q","event_context":"ctx-A"},
            {"id":"R","compact":"r","event_context":"ctx-A"},
            {"id":"S","compact":"s","event_context":"ctx-A"}
        ],
        "pattern_rules": [{"name":"idem","left":"(and ?a ?a)","right":"?a"}],
        "ground_rules": [
            {"name":"eq-p-q","left":"p","right":"q","event_context":"ctx-A","proof_status":"unsat"},
            {"name":"eq-q-r","left":"q","right":"r","event_context":"ctx-A","proof_status":"unsat"}
        ],
        "pairs": [["P","R"],["R","Q"],["Q","S"]]
    })
}

fn invoke_bytes(payload: &[u8]) -> Output {
    let mut child = Command::new(env!("CARGO_BIN_EXE_egg_regression_forms"))
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .unwrap();
    child.stdin.as_mut().unwrap().write_all(payload).unwrap();
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
        graph["targets"].as_array().unwrap().len(),
        data["targets"].as_array().unwrap().len()
    );
    graph
}

#[test]
fn preserves_merged_pair_explanations_on_partial_saturation() {
    let result = graph(&request());
    assert_eq!(result["stop_reason"], "Some(Saturated)");
    let rows = result["targets"].as_array().unwrap();
    assert_eq!(rows[0]["eclass"], rows[1]["eclass"]);
    assert_eq!(rows[1]["eclass"], rows[2]["eclass"]);
    assert_ne!(rows[2]["eclass"], rows[3]["eclass"]);
    let edges = result["rewrite_explanations"].as_array().unwrap();
    assert_eq!(edges.len(), 2);
    assert_eq!(
        (&edges[0]["left"], &edges[0]["right"]),
        (&json!("P"), &json!("R"))
    );
    assert_eq!(
        (&edges[1]["left"], &edges[1]["right"]),
        (&json!("R"), &json!("Q"))
    );
    let first = edges[0]["explanation"].as_str().unwrap();
    assert!(first.starts_with("(and p q)\n"));
    assert!(first.contains("eq-p-q") && first.contains("eq-q-r") && first.contains("idem"));
    let reversed = edges[1]["explanation"].as_str().unwrap();
    assert!(reversed.starts_with("r\n") && reversed.contains("eq-q-r"));
}

#[test]
fn goal_stop_has_only_explicit_pairs_and_structural_identity_needs_no_edge() {
    let mut p = request();
    p["targets"][3]["compact"] = json!("q");
    let result = graph(&p);
    assert_eq!(result["stop_reason"], "Some(Other(\"TargetsMerged\"))");
    assert_eq!(result["rewrite_explanations"].as_array().unwrap().len(), 2);
    assert_eq!(
        result["targets"][1]["eclass_before"],
        result["targets"][3]["eclass_before"]
    );
    assert_eq!(
        result["targets"][1]["eclass"],
        result["targets"][3]["eclass"]
    );
}

#[test]
fn rejects_unknown_duplicate_self_pairs_and_context_mismatch() {
    for invalid in [
        json!([]),
        json!([["P", "P"]]),
        json!([["P", "missing"]]),
        json!([["P", "Q"], ["Q", "P"]]),
        json!([["P", 4]]),
        json!([["P"]]),
    ] {
        let mut p = request();
        p["pairs"] = invalid;
        assert!(!invoke(&p).status.success());
    }
    for (key, value) in [
        ("/targets/2/event_context", json!("ctx-B")),
        ("/targets/2/id", json!("P")),
        ("/targets/2/id", json!(" ")),
        ("/ground_rules/0/event_context", json!("ctx-B")),
        ("/ground_rules/0/proof_status", json!("sat")),
        ("/ground_rules/0/right", json!("(or q r)")),
    ] {
        let mut p = request();
        *p.pointer_mut(key).unwrap() = value;
        let outcome = invoke(&p);
        assert!(!outcome.status.success(), "accepted {key}");
        assert!(outcome.stdout.is_empty());
    }
}

#[test]
fn duplicate_json_keys_rejected_before_processing() {
    let clean = serde_json::to_string(&request()).unwrap();
    let raw = clean.replacen(
        r#""context_id":"ctx-A""#,
        r#""context_id":"ctx-B","context_id":"ctx-A""#,
        1,
    );
    assert_ne!(clean, raw);
    assert!(!invoke_bytes(raw.as_bytes()).status.success());
}
