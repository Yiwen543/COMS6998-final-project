"""Check that proof-impact decisions fail closed on independent evidence or solver conflicts."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import m3_eco_impact as impact


class EcoImpactTests(unittest.TestCase):
    def test_corrupt_replay_evidence_rejected(self):
        sources = {"baseline": "original RTL", "eco": "changed RTL"}
        formal = {
            name: {"rules": {"r": {"status": "unsat"}}, "claims": {"c": {"status": "sat"}}}
            for name in sources
        }
        records = {"cases": {name: {**deepcopy(truth), "source_sha256": impact.sha(sources[name].encode())}
                             for name, truth in formal.items()}}
        self.assertEqual(impact.compare_replay(sources, formal, records)["statuses_checked"], 4)
        for path, value in [
            (("baseline", "source_sha256"), "wrong"),
            (("eco", "claims", "c", "status"), "unsat"),
            (("baseline", "rules", "r", "status"), "unknown"),
            (("baseline", "rules", "r", "status"), None),
            (("eco", "claims", "c"), None),
            (("baseline", "rules"), None),
            (("baseline",), None),
        ]:
            with self.subTest(path=path):
                corrupted = deepcopy(records)
                obj = corrupted["cases"]
                for key in path[:-1]:
                    obj = obj[key]
                if value is None:
                    del obj[path[-1]]
                else:
                    obj[path[-1]] = value
                with self.assertRaisesRegex(ValueError, "independent replay"):
                    impact.compare_replay(sources, formal, corrupted)

    def test_ordinary_recheck_has_its_own_solver_result(self):
        rules = {"r": {"status": "sat"}}
        expected = {"target": {"status": "sat"}}
        receipts = {"target": ["r"]}
        with patch.object(impact, "certify_eco", side_effect=[
                {"rules": rules}, {"claims": expected}, {"claims": {"target": {"status": "unsat"}}}
        ]) as certify:
            with self.assertRaisesRegex(ValueError, "ordinary proof reuse"):
                impact.check_case("RTL", [True], [False], receipts, receipts,
                                  {"rules": rules, "claims": expected})
            self.assertEqual(certify.call_count, 3)
            self.assertEqual(certify.call_args_list[-1].kwargs, {"rule_names": [], "claim_names": ["target"]})


if __name__ == "__main__":
    unittest.main()
