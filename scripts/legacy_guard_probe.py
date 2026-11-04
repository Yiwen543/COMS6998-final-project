"""Exploratory legacy Verilog guard extraction; no qualification or stimulus.

Treat always @* as a lexical combinational context only. This does not replace
it with always_comb, infer temporal equivalence, or expand procedural SSA.
Sequential event controls and original source spans remain unchanged.
"""
import argparse
import json
from pathlib import Path
from slang_guard_adapter import walk
from spi_semantic_v2 import RichAdapter, pair_audit


class LegacyAdapter(RichAdapter):
    def extract(self):
        # Reuse the existing visitor per member, including its fail-closed rules
        # for predicates that read a value assigned earlier in the same process.
        members = self.body['members']
        try:
            for member in members:
                body = member.get('body', {})
                implicit = (member.get('kind') == 'ProceduralBlock'
                            and member.get('procedureKind') == 'Always'
                            and body.get('kind') == 'Timed'
                            and body.get('timing', {}).get('kind') == 'ImplicitEvent')
                if implicit:
                    self.blocking_writes = {n['symbol'].split()[0]
                        for a in walk(body) if a.get('kind') == 'Assignment' and not a.get('isNonBlocking', False)
                        for n in walk(a['left']) if n.get('kind') == 'NamedValue'}
                    self.visit(body['stmt'], 'true', ['combinational:implicit_all'])
                else:
                    self.body['members'] = [member]
                    super().extract()
        finally:
            self.body['members'] = members
        return self


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--ast',type=Path,required=True);p.add_argument('--top',required=True)
    p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=False)
    adapter=LegacyAdapter(json.loads(a.ast.read_text()),a.top).extract()
    data={'targets':adapter.targets,'atoms':adapter.atoms,'unsupported':adapter.unsupported,
          'qualified':False,'scope':'Two-state lexical combinational hypotheses only; no source counter mapping or temporal reachability; no procedural alias expansion.'}
    (a.output/'extraction.json').write_text(json.dumps(data,indent=2)+'\n')
    audit=pair_audit(adapter,a.output,expand_aliases=True,procedural=False)
    (a.output/'audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    print(json.dumps({'targets':len(adapter.targets),'unsupported_entries':len(adapter.unsupported),
          'counts':audit['counts'],'different_expression_pairs':sum(p['source_expressions_differ'] for p in audit['equivalent_pairs']),
          'qualified':False}))
