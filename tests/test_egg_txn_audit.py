"""Archive-integrity checks for blind transaction synthesis and private repair histories."""
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def encode(x):
    return (json.dumps(x, sort_keys=True) + "\n").encode()


class TransactionAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        corpus = ROOT / "results/milestone3/frame-faults"
        location, binary = os.environ.get("EGG_TXN_AUDIT_RUN"), os.environ.get("EGG_TXN_BINARY")
        if not location and not binary:
            raise unittest.SkipTest("set EGG_TXN_AUDIT_RUN (two-round fixture) or EGG_TXN_BINARY")
        from audit_egg_txn import AuditEvidence, audit, read_directory
        if location:
            root = Path(location)
        else:
            from egg_txn_loop import run
            tmp = tempfile.TemporaryDirectory()
            cls.addClassCleanup(tmp.cleanup)
            root = Path(tmp.name) / "experiment"
            run(corpus_dir=corpus, binary=binary, out=root, mode="fixture", trials=1, rounds=2)
        cls.files = read_directory(root)
        cache = AuditEvidence(corpus)
        cls.check = staticmethod(lambda files: audit(files, corpus, cache=cache))
        cls.ok = cls.check(cls.files)
        cls.seed = "trial-01/egg/seed"

    def reject(self, changes, reason):
        self.assertTrue(all(self.files.get(k) != v for k,v in changes.items()))
        with self.assertRaisesRegex(ValueError, reason):
            self.check({**self.files, **changes})

    def test_blind_initial_may_not_contain_shared_seed(self):
        path = "trial-01/initial/request.json"
        r = json.loads(self.files[path])
        r["messages"].append({"role":"user","content":"Initial candidate: " + self.files["trial-01/initial/response.json"].decode()})
        self.reject({path: encode(r)}, "request")

    def test_cannot_substitute_own_initial_or_other_arms_history(self):
        path = "trial-01/egg/round-01/request.json"
        r = json.loads(self.files[path])
        r["messages"][2]["content"] = json.dumps({"monitors": {}})
        self.reject({path: encode(r)}, "request")
        path = "trial-01/egg/round-02/request.json"
        self.reject({path: self.files["trial-01/raw/round-02/request.json"]}, "request")

    def test_heldout_pin_injection_in_common_and_request(self):
        p = "trial-01/raw/seed"
        common = json.loads(self.files[p + "/common.json"])
        common["public"]["visible_rtl_observations"]["F04"] = {"pin": "secret"}
        text = json.dumps(common["public"], sort_keys=True, separators=(",", ":"))
        path = "trial-01/raw/round-01/request.json"
        request = json.loads(self.files[path])
        request["messages"][-1]["content"] = text + "\nSubmit all nine monitors again."
        self.reject({p+"/common.json":encode(common), p+"/feedback.txt":(text+"\n").encode(),
                     path:encode(request)}, "common observation")

    def test_stale_candidate_proof(self):
        path = self.seed+"/certificates.json"
        cert = json.loads(self.files[path])
        names = [n for n,c in cert.items() if c["public"]["status"] == "checked_rewrite"]
        self.assertGreaterEqual(len(names), 2)
        cert[names[1]] = cert[names[0]]
        self.reject({path:encode(cert)}, "bound|proof|certificate|source|cube|request|query|replay")

    def test_changed_domain_or_wrong_xor_endpoints(self):
        import z3
        from audit_egg_txn import check_model
        from egg_txn_terms import REFERENCES
        path = "trial-01/raw/seed/oracles.json"
        records = json.loads(self.files[path])
        monitors = json.loads(self.files["trial-01/initial/response.json"])["output"]["monitors"]
        n = "data_entitlement"
        orig = records[n]
        domain,xor = z3.parse_smt2_string(orig["smt2"])
        for first,second,error in ((z3.BoolVal(False),xor,"domain"),(domain,z3.BoolVal(False),"endpoints")):
            with self.subTest(error=error):
                solver = z3.Solver(); solver.add(first,second)
                with self.assertRaisesRegex(ValueError,error):
                    check_model(REFERENCES[n],monitors[n],{**orig,"smt2":solver.to_smt2()},orig)

    def test_used_receipts_and_fixture_claims(self):
        path = "trial-01/raw/round-01/response.json"
        r = json.loads(self.files[path]);r["usage"]={"input_tokens":25,"output_tokens":2,"total_tokens":27}
        self.reject({path:encode(r)}, "fixture")
        self.reject({"trial-01/ordinary/seed/response.json":self.files["trial-01/initial/response.json"]}, "unexpected archive files")
        s = json.loads(self.files["summary.json"]);s["provider_api_calls"] = s["responses"]
        self.reject({"summary.json":encode(s)}, "summary")

    def test_shared_live_usage_counted_once(self):
        # In-memory synthetic receipt envelopes exercise accounting. No API calls.
        files = dict(self.files)
        config = json.loads(files["config.json"])
        config.update(mode="live", provider={"model":"unit-test","transport":"OpenAI Responses API",
            "reasoning_effort":"low","max_output_tokens":100})
        files["config.json"] = encode(config)
        summary = json.loads(files["summary.json"])
        costs = {a:dict.fromkeys(("input_tokens","output_tokens","total_tokens"),0) for a in ("initial", *config["arms"])}
        for i,path in enumerate(sorted(p for p in files if p.endswith("/response.json")),1):
            arm=path.split("/")[1]
            usage={"input_tokens":10+i,"output_tokens":5,"total_tokens":15+i}
            r=json.loads(files[path]);r.update(id=f"resp_synthetic_{i}",model="unit-test",requested_model="unit-test",
                service_tier="default",status="completed",http_status=200,dispatch_attempted=True,usage=usage)
            for k,v in usage.items():costs[arm][k]+=v
            files[path]=encode(r)
        summary.update(mode="live",model="unit-test",requested_model="unit-test",provider_api_calls=summary["responses"],
            initial_usage=costs["initial"],provider_usage={a:costs[a] for a in config["arms"]})
        files["summary.json"]=encode(summary)
        audited=self.check(files)
        self.assertIsNone(self.ok["live_session_usage"])
        self.assertEqual(audited["new_api_calls"],0)
        for k in costs["initial"]:
            self.assertEqual(audited["provider_total_counting_initial_once"][k],sum(x[k] for x in costs.values()))
            for arm in config["arms"]:
                record=audited["live_session_usage"]["trial-01"]["arms"][arm]
                self.assertEqual(record["including_initial_to_first_verified"][k],
                    record["incremental_to_first_verified"][k]+costs["initial"][k])
        summary["initial_usage"]={k:3*v for k,v in costs["initial"].items()}
        with self.assertRaisesRegex(ValueError,"summary"):
            self.check({**files,"summary.json":encode(summary)})
        first="trial-01/initial/response.json";second="trial-01/raw/round-01/response.json"
        r=json.loads(files[second]);r["id"]=json.loads(files[first])["id"]
        with self.assertRaisesRegex(ValueError,"reused response"):
            self.check({**files,second:encode(r)})

    def test_perfect_or_invalid_initial_is_retained_without_resampling(self):
        # A provider stub returns a predeclared first answer and then exact
        # references. No diagnosis is needed for invalid or fully correct terms.
        from audit_egg_txn import read_directory
        from egg_txn_loop import run
        from egg_txn_terms import REFERENCES
        correct = {"monitors": dict(REFERENCES)}
        for valid in (True, False):
            with self.subTest(perfect=valid), tempfile.TemporaryDirectory() as directory:
                count = 0

                def provider(_messages, _schema):
                    nonlocal count
                    count += 1
                    output = {"monitors": {}} if not valid and count == 1 else correct
                    return {"id": f"resp_synthetic_{count}", "output": output, "status": "completed",
                            "model": "unit-test", "requested_model": "unit-test", "dispatch_attempted": True,
                            "http_status": 200, "usage": {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15}}

                out = Path(directory) / "transcript"
                run(corpus_dir=ROOT / "results/milestone3/frame-faults", binary=sys.executable,
                    out=out, mode="live", trials=1, rounds=1, provider=provider,
                    provider_config={"model":"unit-test", "transport":"OpenAI Responses API",
                                     "reasoning_effort":"low", "max_output_tokens":100})
                result = self.check(read_directory(out))
                self.assertEqual(count, 4)
                self.assertEqual(result["initially_verified_trials"], int(valid))
                for row in result["live_session_usage"]["trial-01"]["arms"].values():
                    self.assertEqual(row["first_verified_round"], 0 if valid else 1)
                    self.assertEqual(row["including_initial_to_first_verified"]["total_tokens"], 15 if valid else 30)


if __name__ == "__main__":
    unittest.main()
