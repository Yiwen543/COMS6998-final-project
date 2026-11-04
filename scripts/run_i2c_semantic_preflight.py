"""Reproduce typed extraction, every pair query, cell cross-check and egg joins."""
import argparse
import json
from pathlib import Path
from probe_i2c_event_candidate import probe
from spi_semantic_v2 import RichAdapter,pair_audit
from i2c_netlist_proof import prove
from certify_i2c_guards import certify


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--calibration',type=Path,required=True)
    a=p.parse_args();out=a.output.resolve()
    probe(out)
    adapter=RichAdapter(json.loads((out/'ast.json').read_text()),'i2c_controller_fsm').extract()
    audit_dir=out/'qfbv-hypotheses';audit_dir.mkdir()
    audit=pair_audit(adapter,audit_dir,expand_aliases=True,procedural=True)
    (audit_dir/'audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    prove(out/'ast.json',out/'netlist.json',out/'netlist-proof')
    certify(out,a.calibration.resolve())


if __name__=='__main__':main()
