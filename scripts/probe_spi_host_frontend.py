#!/usr/bin/env python3
"""Probe unmodified SPI_HOST elaboration without claiming guard integration."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results/natural_ip_parameter_screen_20261103/spi_host_slang"
BASE = ROOT / "third_party/opentitan_candidate/hw/ip"
YOSYS = ROOT / "build/tools/oss-cad-20261103/oss-cad-suite/bin/yosys"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = [BASE / name for name in ("prim/rtl/prim_util_pkg.sv",
        "spi_host/rtl/spi_host_cmd_pkg.sv", "prim_generic/rtl/prim_flop_en.sv",
        "spi_host/rtl/spi_host_fsm.sv")]
    relative = [str(x.relative_to(ROOT)) for x in files]
    inc = str((BASE / "prim/rtl").relative_to(ROOT))
    out = str(OUT.relative_to(ROOT))
    script = (f'read_slang --single-unit --no-proc --top spi_host_fsm -G NumCS=2 '
        f'-D SYNTHESIS -I {inc} ' + ' '.join(relative) +
        f'; write_rtlil -readable {out}/readable.il; proc; write_json {out}/netlist.json')
    (OUT / "probe.ys").write_text(script+'\n')
    run = subprocess.run([str(YOSYS), '-Q', '-T', '-p', script], cwd=ROOT,
                         text=True, capture_output=True, timeout=90)
    (OUT / "probe.log").write_text(run.stdout+run.stderr)
    if run.returncode:
        raise RuntimeError("See saved probe.log")
    netlist = json.loads((OUT/'netlist.json').read_text())['modules']['spi_host_fsm']
    if len(netlist['ports']['csb_o']['bits']) != 2 or len(netlist['ports']['command_i']['bits']) != 56:
        raise AssertionError("Elaborated fixed interface widths disagree")
    il = (OUT/'readable.il').read_text()
    sync = len(re.findall(r'^    sync ',il,re.M))
    flops = len(re.findall(r'^  cell \$(?:a[dl]?dff|dff)',il,re.M))
    argv = ['verilator','--lint-only','--timing','-Wno-fatal','--top-module','spi_host_fsm',
            '-GNumCS=2','-DSYNTHESIS','-I'+inc,*relative]
    lint = subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,timeout=90)
    (OUT/'verilator-lint.log').write_text(lint.stdout+lint.stderr)
    sources = files + [BASE/'prim/rtl'/x for x in ('prim_assert.sv','prim_assert_dummy_macros.svh',
                                                 'prim_assert_sec_cm.svh','prim_flop_macros.sv')]
    status = {'status':'elaboration_passed_adapter_incomplete',
        'yosys':subprocess.check_output([str(YOSYS),'-V'],text=True).strip(),
        'release':json.loads((YOSYS.parents[2]/'provenance.json').read_text()),
        'sources_sha256':{str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in sources},
        'parameters':{'NumCS':2},'verified_port_widths':{'csb_o':2,'command_i':56},
        'defines':['SYNTHESIS'],
        'assertion_scope':'Upstream embedded assertion macros excluded for elaboration; this is not formal proof or a specification checker.',
        'verilator_lint_returncode':lint.returncode,'verilator_command':argv,
        'process_sync_records':sync,'flop_cells':flops,
        'source_mapping':'Original source attributes retained, but case spans may anchor statements rather than predicate locations.',
        'blocker':'Existing parser expects native pre-proc switch/case conventions and sync events. Slang has already emitted flop cells, so a reviewed adapter must reconstruct event/reset context and validate branch mappings. No groups are promoted.',
        'qualified_for_model_trial':False,'model_calls':0}
    (OUT/'probe.json').write_text(json.dumps(status,indent=2)+'\n')
    print(json.dumps({k:status[k] for k in ('status','verified_port_widths','verilator_lint_returncode','process_sync_records','flop_cells','qualified_for_model_trial')},indent=2))


if __name__=='__main__':
    main()
