"""Controls for four-state observations at FIFO backpressure boundaries."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from egg_fifo_replay import inspect, input_rows


class FifoReplayTests(unittest.TestCase):
    def test_yw_input_packing_with_initial_only_state(self):
        # The lowest bits are the first declaration. The initial-only memory bit
        # sits above all input ports and is absent at later steps.
        widths = [("s_axis_tdata", 8), ("m_axis_tready", 1), ("rst", 1),
                  ("s_axis_tlast", 1), ("s_axis_tuser", 1), ("s_axis_tvalid", 1)]
        signals = [{"path": ["\\" + n], "width": w, "offset": 0, "init_only": False} for n, w in widths]
        signals.append({"path": ["\\dut", "\\memory"], "width": 1, "offset": 0, "init_only": True})
        witness = {"format": "Yosys Witness Trace", "signals": signals,
                   "clocks": [{"path": ["\\clk"], "edge": "posedge", "offset": 0}],
                   "steps": [{"bits": "x0001010100101"}, {"bits": "1110100111100"}]}
        first, second = input_rows(witness)
        self.assertEqual((first["s_axis_tdata"], first["rst"], first["m_axis_tready"]), (0xa5, 1, 0))
        self.assertEqual((second["s_axis_tdata"], second["s_axis_tlast"], second["m_axis_tready"]), (0x3c, 1, 1))
        witness["steps"][1]["bits"] = "111010011110x"
        with self.assertRaisesRegex(ValueError, "unknown/incomplete"):
            input_rows(witness)

    def test_valid_stall_and_unknown_payload(self):
        previous = dict(rst="0", s_axis_tvalid="0", m_axis_tvalid="1", m_axis_tready="0",
                        m_axis_tdata="11000001", m_axis_tlast="1", m_axis_tuser="0")
        current = dict(previous, m_axis_tdata="11000000", m_axis_tready="1")
        self.assertEqual(inspect([previous, current])[0]["violated"], ["data_changed"])
        unknown = dict(current, m_axis_tdata="xxxxxxx0")
        with self.assertRaisesRegex(ValueError, "inconclusive"):
            inspect([previous, unknown])
        self.assertEqual(inspect([dict(previous, m_axis_tvalid="0"), unknown]), [])
        self.assertEqual(inspect([previous, dict(unknown, rst="1")]), [])
