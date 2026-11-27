"""Check Yosys witness packing at the boundary between formal and physical replay."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from egg_fifo_formal import INPUTS, input_rows


class FifoFormalWitnessTests(unittest.TestCase):
    def test_omitted_memory_bits_and_unknown_external_pins(self):
        pins = {"clk": 1, **INPUTS}
        signals = [{"path": ["\\" + key], "width": width, "offset": 0, "init_only": False}
                   for key, width in pins.items()]
        signals.append({"path": ["\\dut", "\\mem", "\\[0]"], "width": 10, "offset": 0, "init_only": True})
        values = {"clk": 0, "rst": 1, "s_axis_tvalid": 1, "s_axis_tdata": 0x95,
                  "s_axis_tlast": 0, "s_axis_tuser": 1, "m_axis_tready": 0}
        packed = "".join(f"{values[key]:0{width}b}" for key, width in reversed(pins.items()))
        # Missing high bits in the native YW format are unknown. Here they
        # belong to internal RAM; all primary inputs are still concrete.
        witness = {"clocks": [{"path": ["\\clk"], "edge": "posedge", "offset": 0}],
                   "signals": signals, "steps": [{"bits": packed}]}
        self.assertEqual(input_rows(witness), [{k: values[k] for k in INPUTS}])
        corrupted = copy.deepcopy(witness)
        corrupted["steps"][0]["bits"] = packed[1:]
        with self.assertRaisesRegex(ValueError, "ambiguous witness input m_axis_tready"):
            input_rows(corrupted)


if __name__ == "__main__":
    unittest.main()
