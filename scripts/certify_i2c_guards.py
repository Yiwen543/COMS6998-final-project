"""Certify all preselected I2C hypotheses before calibration/model selection."""
import json
import subprocess
from collections import defaultdict
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from run_i2c_fixed import SOURCE,verify_source
from coverage import load,summary
from preflight_spi_host import identity,resolve_clock_alias
from screen_spi_semantic_v2 import mapping
from preflight_heldout import verify_rewrites


def certify(base,cal):
    verify_source()
    audit=json.loads((base/'qfbv-hypotheses/audit.json').read_text())
    proof=json.loads((base/'netlist-proof/proof.json').read_text())
    if proof['status']!='pass' or not proof['environment_satisfiable']:raise ValueError('Netlist proof incomplete')
    targets={t['id']:t for t in audit['supported_targets']}
    statuses={tuple(sorted(p)):s for p,s in zip(audit['pair_order'],audit['statuses'])}
    net=json.loads((base/'netlist.json').read_text())['modules']['i2c_controller_fsm']
    clocks=[]
    for name,c in net['cells'].items():
        if c['type']!='$aldff':continue
        clk,aliases=resolve_clock_alias(c['connections']['CLK'],net)
        rst,reset_aliases=resolve_clock_alias(c['connections']['ALOAD'],net)
        valid=(clk==net['ports']['clk_i']['bits'] and rst==net['ports']['rst_ni']['bits']
               and int(c['parameters']['CLK_POLARITY'],2)==1 and int(c['parameters']['ALOAD_POLARITY'],2)==0)
        clocks.append({'cell':name,'valid':valid,'clock_aliases':aliases,'reset_aliases':reset_aliases,
                       'q_bits':c['connections']['Q'],'reset_data_bits':c['connections']['AD']})
    if not clocks or not all(c['valid'] for c in clocks):raise ValueError('Unproved clock/reset context')
    rules=[]
    for p in audit['equivalent_pairs']:
        if not p['source_expressions_differ']:continue
        a,b=targets[p['left']],targets[p['right']]
        if a['event_context']!=b['event_context'] or statuses[tuple(sorted((a['id'],b['id'])))]!='unsat':
            raise ValueError('Unproved relation')
        rules.append({'name':'qfbv-'+a['id']+'-'+b['id'],'left':a['compact'],'right':b['compact'],
          'proof_status':'unsat','event_context':a['event_context'],'pair_proof':'qfbv-hypotheses/pairs.smt2','source_ids':[a['id'],b['id']]})
    payload={'targets':list(targets.values()),'verified_rules':rules}
    (base/'egg-input.json').write_text(json.dumps(payload,indent=2)+'\n')
    p=subprocess.run([str(ROOT/'egraph/target/debug/guard_proofs')],input=json.dumps(payload),text=True,capture_output=True,timeout=30,check=True)
    graph=json.loads(p.stdout);(base/'egg.json').write_text(json.dumps(graph,indent=2)+'\n')
    roots={t['id']:t for t in graph['targets']};buckets=defaultdict(list)
    for t in targets.values():buckets[(tuple(t['event_context']),roots[t['id']]['eclass'])].append(t)
    points=load(cal/'seed.dat',str(SOURCE.relative_to(ROOT)),include_descendants=True)
    mappings={tid:mapping(t,points) for tid,t in targets.items()}
    index={identity(p):p for p in points}
    groups=[]
    for (ctx,ec),members in buckets.items():
        if len({(m['source'],m['line'],m['column']) for m in members})<2:continue
        for i,a in enumerate(members):
            for b in members[i+1:]:
                if statuses.get(tuple(sorted((a['id'],b['id']))))!='unsat':raise ValueError('Unproved egg merge')
        groups.append({'eclass':ec,'event_context':ctx,'member_ids':[t['id'] for t in members],
                       'source_lines':[t['line'] for t in members],
                       'nontrivial':len({roots[t['id']]['eclass_before'] for t in members})>1})
    pair_records=[]
    for rule in rules:
        pair_records.append({'proof':'unsat','egg_same_class':len({roots[i]['eclass'] for i in rule['source_ids']})==1,
            'members':[{'target':targets[i],'mapping':mappings[i]} for i in rule['source_ids']]})
    result={'status':'combinational_certified; event reachability and checker gate separate',
       'different_expression_pairs':pair_records,'counts':audit['counts'],'source_mappings':mappings,'groups':groups,
       'mapped_targets':sum(m['status']=='mapped' for m in mappings.values()),'unresolved_targets':sum(m['status']!='mapped' for m in mappings.values()),
       'clock_reset':clocks,'rewrite_validation':verify_rewrites(),'raw_seed_coverage':summary(points),
       'proof_scope':'Two-state typed combinational SSA under arbitrary current FF/input values; no four-state or temporal equivalence claim. Independent Yosys-cell encoding shares Slang frontend.',
       'discovery_attribution':'QF_BV discovers/proves ground relations; bounded egg saturation organizes certified equalities. All original raw source counters kept separately.',
       'hashes':{str(p.relative_to(ROOT)):sha(p) for p in [SOURCE,Path(__file__),ROOT/'scripts/i2c_netlist_proof.py',base/'qfbv-hypotheses/audit.json',base/'netlist-proof/proof.json',base/'egg-input.json',base/'egg.json']}}
    (base/'certified-guards.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'pairs':len(pair_records),'mapped':result['mapped_targets'],'unresolved':result['unresolved_targets'],'groups':len(groups),'nontrivial':sum(g['nontrivial'] for g in groups)}))


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--calibration',type=Path,required=True)
    a=p.parse_args();certify(a.base.resolve(),a.calibration.resolve())
