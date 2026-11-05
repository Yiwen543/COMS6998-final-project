"""Conditional index domain, bound to an original-transition induction proof.

Only the registered request[N][mindex[N]] site is extended. Invalid selections
remain arbitrary. Import ONLY the proved activation implication, no witnesses.
"""
import hashlib
import json
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from prove_wbxbar_index import SCOPE,configuration
from transaction_semantics import TransactionAdapter,TransactionBitVectors,ObservationNetlist
from spi_semantic_v2 import BitVectors,stable
from slang_guard_adapter import Unsupported,walk

FORMAL=ROOT/'results/wbxbar_conditional_20261104/formal-final'
CERTIFICATE=ROOT/'results/wbxbar_conditional_20261104/domain-certificate.json'
LEMMA='forall N in {0,1}: (!grant[N][2] && mgrant[N]) => unsigned(mindex[N]) <= 2'

def certify():
    configuration();manifest=json.loads((FORMAL/'manifest.json').read_text())
    assert manifest['proof_activation']=='selected' and manifest['assumptions']==[]
    hashes=dict(manifest['hashes']);hashes[str(FORMAL/'manifest.json')]=sha(FORMAL/'manifest.json')
    for task,expect in [('prove','PASS'),('strengthened','PASS'),('false_active','FAIL'),('unconditional','FAIL'),('activation','PASS')]:
        r=json.loads((FORMAL/(task+'-result.json')).read_text());assert r['returncode']==0 and r['status'].split()[0]==expect
        assert r['scope_sha256']==sha(SCOPE) and r['sby_sha256']==sha(FORMAL/(task+'.sby'))
        assert r['invocation_log_sha256']==sha(FORMAL/(task+'-invocation.log'))
        if task in ('prove','strengthened'):
            for phase in ('basecase','induction'):
                log=FORMAL/task/'engine_0'/('logfile_'+phase+'.txt');assert 'Status: passed' in log.read_text()
        for p in (FORMAL/task).rglob('*'):
            if p.is_file():hashes[str(p)]=sha(p)
        for p in [FORMAL/(task+'-result.json'),FORMAL/(task+'.sby'),FORMAL/(task+'-invocation.log')]:hashes[str(p)]=sha(p)
    for p,h in hashes.items():assert sha(Path(p))==h,('proof drift',p)
    r={'status':'inductive_conditional_domain_certified','lemma':LEMMA,'scope_sha256':sha(SCOPE),
       'assumptions':[],'import_helpers':False,'initial_state':'original initial assignments only; no mindex initialization',
       'coverage_witnesses':'private proof controls; never stimulus/prompt material','hashes':hashes}
    if CERTIFICATE.exists():raise ValueError('Do not overwrite certificate')
    CERTIFICATE.write_text(json.dumps(r,indent=2)+'\n');return r

def verify_certificate(path=None):
    path=path or CERTIFICATE;r=json.loads(path.read_text())
    if r['status']!='inductive_conditional_domain_certified' or r['lemma']!=LEMMA or r['scope_sha256']!=sha(SCOPE) or r['assumptions'] or r['import_helpers']:
        raise ValueError('Invalid conditional certificate')
    for p,h in r['hashes'].items():
        if sha(Path(p))!=h:raise ValueError('Conditional proof provenance drift: '+p)
    configuration();return r

class ConditionalAdapter(TransactionAdapter):
    def __init__(self,ast,top,net):
        verify_certificate();self.conditional_selects=[]
        if top!='wbxbar':raise Unsupported('Conditional certificate belongs only to wbxbar')
        super().__init__(ast,top,net)

    def typed(self,node):
        if node['kind']=='ElementSelect' and self.source(node).get('source','').endswith('/wbxbar.v') and self.source(node).get('line')==888:
            value=super().typed(node['value']);sel=super().typed(node['selector'])
            if value['kind']=='Slice' and value['value'].get('symbol')=='request':
                if not (value['type']['width']==3 and sel['kind']=='Slice' and sel['value'].get('symbol')=='mindex'
                        and sel['type']['width']==2 and not sel['type']['signed'] and value['offset'] in (0,3)
                        and sel['offset']==(value['offset']//3)*2):raise Unsupported('Registered select shape drift')
                n=1-value['offset']//3;src=self.source(node)
                out={'kind':'PartialSelect','type':self.type_info(node['type']),'value':value,'selector':sel,'maximum':2,
                     'source':src,'master':n,'certificate_sha256':sha(CERTIFICATE)}
                self.conditional_selects.append(out);return out
        return super().typed(node)

    def state_node(self,name):
        n=next(n for n in walk(self.body) if n.get('kind')=='NamedValue' and n['symbol'].split(' ',1)[1]==name)
        return self.typed(n)

    def extract(self):
        result=super().extract()
        # Explicit level-sensitive event lists are not clock edges and are not
        # promoted to always_comb. Preserve their source records as unsupported.
        withheld=[t for t in self.targets if any(e.startswith('None:') for e in t['event_context'])]
        self.targets=[t for t in self.targets if t not in withheld]
        for t in withheld:self.unsupported.append({'reason':'explicit sensitivity event context not certified; not a clock edge',
            'scope':'target withheld, original counter retained','target':t})
        return result

class ConditionalBitVectors(TransactionBitVectors):
    def term(self,node):
        if node['kind']=='PartialSelect':
            if node['maximum']!=2 or node['certificate_sha256']!=sha(CERTIFICATE):raise Unsupported('Conditional bound/certificate drift')
            v,s=node['value'],node['selector'];a,b=self.term(v),self.term(s)
            u={'kind':'ArbitrarySelectValue','type':node['type'],'symbol':'invalid_select_'+str(node['master']),
               'declaration':node['source']}
            k=self.name(u);self.variables[k]=u
            selected=f'((_ extract 0 0) (bvlshr {a} ((_ zero_extend 1) {b})))'
            return f'(ite (bvule {b} #b10) {selected} {k})'
        return super().term(node)

    def domain_assertions(self):
        ns={n:self.adapter.state_node(n) for n in ('mgrant','grant','mindex')}
        if {n:v['type']['width'] for n,v in ns.items()}!={'mgrant':2,'grant':6,'mindex':4}:raise Unsupported('State-domain width drift')
        # Declarations: mgrant[1:0], grant[0:1][2:0], mindex[0:1][1:0].
        for name in ('grant','mindex'):
            if self.adapter.array_bindings[name]['type']['range']!='[0:1]':raise Unsupported('State-domain array direction drift')
        t={n:self.term(v) for n,v in ns.items()};result=[]
        for n in (0,1):
            idx=f'((_ extract {(1-n)*2+1} {(1-n)*2}) {t["mindex"]})'
            active=f'(= ((_ extract {n} {n}) {t["mgrant"]}) #b1)'
            pseudo=f'(= ((_ extract {(1-n)*3+2} {(1-n)*3+2}) {t["grant"]}) #b1)'
            result.append(f'(assert (or {pseudo} (not {active}) (bvule {idx} #b10)))')
        return result

    def guards(self):
        constraints=self.domain_assertions();h,t,u=super().guards()
        return h+'\n'.join(constraints)+'\n',t,u

class ConditionalNetlist(ObservationNetlist):
    def symbol(self,n):
        if n['kind']=='ArbitrarySelectValue':
            key='invalid_ast_'+stable(n);
            if key not in self.unknown_bits:self.unknown_bits.append(key)
            return key
        return super().symbol(n)

    def cell(self,name):
        c=self.module['cells'][name];p=c.get('connections',{});src=c.get('attributes',{}).get('src','')
        if c['type']!='$shiftx' or not src.startswith('third_party/wb2axip_candidate/rtl/wbxbar.v:888.'):
            return super().cell(name)
        if (len(p['A']),len(p['B']),len(p['Y']))!=(3,2,1) or int(c['parameters']['B_SIGNED'],2):raise Unsupported('Exact independent select shape drift')
        key='n_'+stable(name)
        if key in self.macros:return key,1
        if name in self.active:raise Unsupported('Combinational cycle')
        self.active.add(name)
        try:
            a,b=self.word(p['A']),self.word(p['B']);undef='invalid_net_'+stable(name);self.unknown_bits.append(undef)
            value=f'((_ extract 0 0) (bvlshr {a} ((_ zero_extend 1) {b})))'
            self.macros[key]=f'(define-fun {key} () (_ BitVec 1) (ite (bvule {b} #b10) {value} {undef}))'
            self.used_cells.add(name);self.evidence.append({'cell':name,'source':src,'invalid':'independent arbitrary bit',
                'scope':'Only conditional domain permits proof; no unconditional select bound claimed'})
            return key,1
        finally:self.active.remove(name)

if __name__=='__main__':
    r=certify();print(json.dumps({'status':r['status'],'lemma':r['lemma'],'hashed_files':len(r['hashes'])},indent=2))
