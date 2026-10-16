#!/usr/bin/env python3
from pathlib import Path
root = Path(__file__).resolve().parents[1]
case = root/'examples/arbiter'
graph_path=root/'results/step1/egraph.json'
if not graph_path.exists(): raise SystemExit('Run make step1 first to produce the real E-graph.')
text=(root/'prompts/step1.md').read_text()
text+='\n[SPECIFICATION]\n'+(case/'docs/specification.md').read_text()
text+='\n[RTL_CODE]\n```systemverilog\n'+(case/'rtl/fixed_priority_arbiter.sv').read_text()+'\n```\n'
text+='\n[E_GRAPH_REPRESENTATION]\n```json\n'+graph_path.read_text()+'```\n'
out=root/'results/step1/initial-prompt.md'
out.write_text(text)
print(out)
