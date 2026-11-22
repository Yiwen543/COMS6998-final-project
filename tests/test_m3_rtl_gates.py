"""Regression controls for accepting RTL benchmark observations."""
import os
import shlex
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from benchmark_m3_rtl import REFERENCE, archived_quality, check_archived_replay, normalize, observation
from coverage import DUT_SOURCE, load, summary
from predicates import ROOT, extract


class RtlAcceptanceTests(unittest.TestCase):
    def test_archived_dut_counter_identity_and_multiplicity(self):
        archive = archived_quality(REFERENCE)["initial"]
        lines = (REFERENCE / "initial.dat").read_text().splitlines()
        log = (REFERENCE / "initial.log").read_text()
        # Choose an actual covered counter. Neither mutation changes its hit status.
        index = next(i for i, line in enumerate(lines)
                     if DUT_SOURCE in line and not line.endswith("' 0") and "\x01page\x02" in line)
        original = lines[index]
        fields, hits = original.rsplit("' ", 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "initial.dat"
            path.write_text("\n".join([lines[0], *reversed(lines[1:])]) + "\n")
            check_archived_replay(path, observation(load(path), log), archive)
            for label, different in [
                ("hit count", f"{fields}' {int(hits) + 1}"),
                ("raw identity", original.replace("\x01page\x02", "\x01page\x02other-", 1)),
            ]:
                with self.subTest(change=label):
                    lines[index] = different
                    path.write_text("\n".join(lines) + "\n")
                    live = observation(load(path), log)
                    self.assertEqual(summary(live["points"]), summary(archive["points"]))
                    with self.assertRaisesRegex(ValueError, "historical DUT counter"):
                        check_archived_replay(path, live, archive)

    def test_misrouted_real_engine_mode(self):
        engine = Path(os.environ.get("GUARD_PROOFS_FAST", ROOT / "egraph/target/release/guard_proofs_fast"))
        if not engine.is_file():
            self.skipTest("build guard_proofs_fast and set GUARD_PROOFS_FAST")
        targets = extract()
        _, _, timing = normalize(targets, "indexed", engine.resolve(), None)
        self.assertEqual(timing["mode"], "indexed")
        with tempfile.TemporaryDirectory() as directory:
            wrapper = Path(directory) / "wrong-mode"
            # The real engine produces correct proof bytes in spanning mode.
            wrapper.write_text(f"#!/bin/sh\nexec {shlex.quote(str(engine.resolve()))} spanning\n")
            wrapper.chmod(0o700)
            with self.assertRaisesRegex(ValueError, "requested mode 'indexed'"):
                normalize(targets, "indexed", wrapper, None)


if __name__ == "__main__":
    unittest.main()
