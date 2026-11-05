import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from wbxbar_conditional_semantics import ConditionalAdapter,ConditionalBitVectors,verify_certificate,CERTIFICATE,LEMMA
BASE=ROOT/'results/wbxbar_conditional_20261104/screen-v2'

class ConditionalDomainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a=ConditionalAdapter(json.loads((BASE/'ast.json').read_text()),'wbxbar',json.loads((BASE/'flat.json').read_text())['modules']['wbxbar']).extract()

    def test_certificate_lemma_and_provenance_fail_closed(self):
        valid=verify_certificate();self.assertEqual(valid['lemma'],LEMMA)
        for which in ('lemma','hash'):
            bad=copy.deepcopy(valid)
            if which=='lemma':bad['lemma']='unsigned(mindex) <= 2 unconditionally'
            else:bad['hashes'][next(iter(bad['hashes']))]='0'*64
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/'certificate.json';p.write_text(json.dumps(bad))
                with self.assertRaises(ValueError):verify_certificate(p)

    def test_exact_select_domain_and_no_clock_fabrication(self):
        rows=self.a.conditional_selects
        self.assertEqual({r['master'] for r in rows},{0,1})
        self.assertTrue(all(r['source']['line']==888 and r['maximum']==2 and r['selector']['type']['width']==2 for r in rows))
        self.assertFalse(any(e.startswith('None:') for t in self.a.targets for e in t['event_context']))
        dropped=[r['target'] for r in self.a.unsupported if 'target' in r]
        self.assertEqual(len(dropped),16)
        self.assertTrue(all(any(e.startswith('None:') for e in t['event_context']) for t in dropped))

    def test_modified_bound_cannot_reuse_certificate(self):
        m=ConditionalBitVectors(self.a,procedural=True);row=copy.deepcopy(self.a.conditional_selects[0]);row['maximum']=1
        with self.assertRaisesRegex(Exception,'bound/certificate drift'):m.term(row)

    def test_removing_lemma_exposes_definition_mismatch(self):
        proof=json.loads((BASE/'proof/proof.json').read_text());query=(BASE/'proof/proof.smt2').read_text()
        self.assertEqual(proof['status'],'pass');self.assertEqual(len(proof['domain_assertions']),2)
        for assertion in proof['domain_assertions']:
            self.assertEqual(query.count(assertion),1);query=query.replace(assertion,'; removed domain for negative control')
        p=subprocess.run(['z3','-in'],input=query,text=True,capture_output=True,timeout=60,check=True)
        statuses=p.stdout.splitlines();self.assertEqual(statuses[0],'sat')
        bad=[r['symbol'] for r,s in zip(proof['definition_checks'],statuses[1:]) if s=='sat']
        self.assertIn('m_stall',bad)

    def test_only_primary_lemma_imported(self):
        m=ConditionalBitVectors(self.a,procedural=True);header,targets,unsupported=m.guards()
        self.assertEqual(unsupported,[])
        self.assertEqual(len(m.domain_assertions()),2)
        self.assertNotIn('onehot',header)
        self.assertTrue(any(v['kind']=='ArbitrarySelectValue' for v in m.variables.values()))
        self.assertEqual(len(targets),len(self.a.targets))

if __name__=='__main__':unittest.main()
