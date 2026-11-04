import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from txuart_fixture import check


class TxuartCheckerFaultTests(unittest.TestCase):
    def test_public_pin_data_flip_is_detected(self):
        evidence = ROOT / "results/next_natural_ip_screen/txuart"
        vectors = evidence / "calibration.vectors"
        log = evidence / "calibration.sim.log"
        if not vectors.exists() or not log.exists():
            self.skipTest("run TX UART preflight first")
        actions = [dict(zip(("reset", "break", "wr", "data"), map(int, line.split())))
                   for line in vectors.read_text().splitlines()]
        original = log.read_text()
        self.assertEqual([], check(actions, original)["failures"])
        lines = original.splitlines()
        trace_indices = [i for i, line in enumerate(lines) if line.startswith("TRACE ")]
        tx = [int(lines[i].split()[-1]) for i in trace_indices]
        start = next(i for i in range(1, len(tx)-3) if tx[i-1] == 1 and tx[i] == 0)
        sample_line = trace_indices[start + 3]
        fields = lines[sample_line].split()
        fields[-1] = str(1 - int(fields[-1]))
        lines[sample_line] = " ".join(fields)
        defects = check(actions, "\n".join(lines))["distinct_defects"]
        self.assertIn("uart_data", defects)


if __name__ == "__main__":
    unittest.main()
