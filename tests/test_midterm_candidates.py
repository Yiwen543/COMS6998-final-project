"""Provenance and semantic-location checks for the outcome-blind candidate screen."""
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from coverage import load  # noqa: E402


class MidtermCandidateTests(unittest.TestCase):
    def test_pinned_originals_match_dataset(self):
        lock = json.loads((ROOT / "docs/midterm-candidate-lock.json").read_text())
        raw = (ROOT / ".cache" / lock["dataset_file"]).read_bytes()
        self.assertEqual(lock["dataset_sha256"], hashlib.sha256(raw).hexdigest())
        rows = raw.splitlines(keepends=True)
        for item in lock["candidates"]:
            row = rows[item["record_line"] - 1]
            self.assertEqual(item["record_sha256"], hashlib.sha256(row).hexdigest())
            record = json.loads(row)
            self.assertEqual(item["id"], record["id"])
            for field, digest in item["fields"].items():
                area, name = field.split("/", 1)
                path = ROOT / "examples" / item["slug"] / (
                    "rtl" if name.endswith((".sv", ".v")) else "docs") / Path(name).name
                self.assertEqual(digest, hashlib.sha256(path.read_bytes()).hexdigest())
                self.assertEqual(record[area][name].encode(), path.read_bytes())

    def test_dut_descendants_are_included_without_testbench_leakage(self):
        sep, split = "\x01", "\x02"
        def row(hier, hits):
            fields = {"f": "rtl/demo.sv", "l": "5", "n": "1", "t": "line",
                      "o": "block", "h": hier}
            packed = sep.join(k + split + v for k, v in fields.items())
            return f"C '{packed}' {hits}\n"
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "coverage.dat"
            path.write_text("# SystemC::Coverage-3\n" +
                            row("TOP.tb.dut.child", 2) + row("TOP.tb.other", 9))
            points = load(path, "rtl/demo.sv", include_descendants=True)
            self.assertEqual(1, len(points))
            self.assertEqual(2, points[0]["hits"])

    def test_each_ip_has_proved_seed_uncovered_reachable_group(self):
        data = json.loads((ROOT / "results/midterm_candidate_preflight/selection.json").read_text())
        self.assertEqual(2, len({ip["id"] for ip in data["ips"]}))
        for ip in data["ips"]:
            qualifying = []
            for group in ip["groups"]:
                members = group["members"]
                if len({(m["line"], m["column"]) for m in members}) < 2:
                    continue
                if all(m["seed_coverage"]["status"] == "mapped" and
                       m["seed_coverage"]["hits"] == 0 and
                       m["calibration_coverage"]["status"] == "mapped" and
                       m["calibration_coverage"]["hits"] > 0 for m in members):
                    self.assertEqual(len(members) - 1, group["z3_pair_checks"])
                    qualifying.append(group)
            self.assertTrue(qualifying, ip["id"])


if __name__ == "__main__":
    unittest.main()
