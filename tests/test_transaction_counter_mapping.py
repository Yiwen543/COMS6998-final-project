import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from transaction_counter_mapping import CounterRegistry
from screen_write_hierarchy import join_counter,aggregate
from preflight_spi_host import identity


def fixture(folder,missing=False,collision=False):
    # Both printable wildcards match genblk.ram_arb_inst. Only the
    # specialization metadata identifies the correct physical counter.
    rows=[('v_branch/arbiter_A','tb.dut.*_arb_inst',['m[0].cmd_arb_inst','m[1].cmd_arb_inst']),
          ('v_branch/arbiter_B','tb.dut.genblk*_arb_inst',['genblk.ram_arb_inst'])]
    points=[];raw=['# SystemC::Coverage-3'];cpp=[]
    for index,(page,hier,scopes) in enumerate(rows):
        f={'f':'rtl/arbiter.v','l':'114','n':'14','t':'branch','page':page,'o':'if','S':'114,116','h':hier}
        raw.append("C '"+''.join('\x01'+k+'\x02'+v for k,v in f.items())+"' 0")
        points.append({'source':f['f'],'line':114,'column':14,'type':'branch','outcome':'if','hierarchy':hier,'span':f['S'],'hits':0})
        for scope in scopes:
            if missing and scope.startswith('genblk'):continue
            args=['ptr','first','true',json.dumps(f['f']),'114','14',json.dumps('.tb.dut.'+scope),json.dumps(page),'"if"','"114,116"','""','""','""','""']
            cpp.append('vlSelf->__vlCoverInsert('+', '.join(args)+');')
    if collision:raw.append(raw[-1].replace('arbiter_B','arbiter_C'))
    r=folder/'seed.dat';r.write_text('\n'.join(raw)+'\n');b=folder/'cpp';b.mkdir();(b/'inserts.cpp').write_text('\n'.join(cpp))
    return CounterRegistry(r,b,points),points

def target(scope,id='t'):
    return {'id':id,'instance_scope':scope,'outcome':'if','counter_anchor':{'source':'rtl/arbiter.v','line':114,'column':14},
            'event_context':['combinational'],'compact':'true','local_compact':'true'}

class CounterMappingTests(unittest.TestCase):
    def test_overlapping_wildcard_is_not_a_membership_rule(self):
        with tempfile.TemporaryDirectory() as d:
            registry,points=fixture(Path(d));scopes=['m[0].cmd_arb_inst','m[1].cmd_arb_inst','genblk.ram_arb_inst'];instances=[{'path':s} for s in scopes]
            for s,p in zip(scopes,[points[0],points[0],points[1]]):
                result=registry.join(join_counter,target(s),points,instances)
                self.assertEqual(result['status'],'mapped');self.assertEqual(result['point'],p)
            bad=target('genblk.impostor_arb_inst')
            self.assertEqual(registry.join(join_counter,bad,points,instances+[{'path':bad['instance_scope']}])['status'],'unresolved')

    def test_partial_instance_guard_union_is_not_admitted(self):
        with tempfile.TemporaryDirectory() as d:
            registry,points=fixture(Path(d));scopes=['m[0].cmd_arb_inst','m[1].cmd_arb_inst'];instances=[{'path':s} for s in scopes]
            ts=[target(s,'t'+str(i)) for i,s in enumerate(scopes)]
            maps={t['id']:registry.join(join_counter,t,points,instances) for t in ts}
            partial=copy.deepcopy(maps);result,m=registry.aggregate(aggregate,ts[:1],partial,instances)
            self.assertEqual(m['g0']['status'],'unresolved')
            result,m=registry.aggregate(aggregate,ts,maps,instances)
            self.assertEqual(len(result),1);self.assertEqual(m['g0']['point'],points[0]);self.assertEqual(len(points),2)

    def test_missing_insertions_and_colliding_raw_identity_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            registry,points=fixture(Path(d),missing=True)
            self.assertNotIn(identity(points[1]),registry.records)
            self.assertTrue(registry.unresolved)
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError,'identity collision'):fixture(Path(d),collision=True)

if __name__=='__main__':unittest.main()
