"""The frame driver must hold already-offered data over stalls and preserve X/Z."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from egg_frame_replay import parse_log


class FrameDriverObservationTests(unittest.TestCase):
    def test_queue_advances_only_after_observed_handshake(self):
        # Two source bytes are offered on successive clocks. The first is
        # blocked for one clock and remains on the pins when byte two is queued.
        actions = [(0, 1, 17, 0, 0, 0), (0, 1, 33, 1, 0, 0), (0, 0, 0, 0, 1, 1)]
        output = " x 0 z 0 0 0 0 0"
        lines = []
        for i, (data, last, sink, ready, head, tail) in enumerate(
                [(17, 0, 0, 0, 0, 1), (17, 0, 0, 1, 1, 2), (33, 1, 1, 1, 2, 2)]):
            lines.extend([f"PRE {i} 0 1 {data} {last} {sink} {sink} {ready}" + output,
                          f"POST {i} {ready}" + output, f"QUEUE {i} {head} {tail}"])
        log = "\n".join([*lines, "DRIVER_COMPLETE 3"])
        rows, counts = parse_log(log, actions)
        self.assertEqual(counts, [2, 2])
        self.assertEqual(rows[0]["pre"]["m_data"], -1)
        self.assertEqual(rows[0]["post"]["m_last"], -1)
        with self.assertRaisesRegex(ValueError, "lost an offered beat"):
            parse_log(log.replace("PRE 1 0 1 17 0", "PRE 1 0 1 33 1"), actions)
        with self.assertRaisesRegex(ValueError, "driver queue disagrees"):
            parse_log(log.replace("QUEUE 0 0 1", "QUEUE 0 1 1"), actions)
