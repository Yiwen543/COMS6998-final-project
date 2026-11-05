"""New-scope array/wire view, certified against independent Yosys cells.

Only unpacked arrays actually emitted as named flattened wires are admitted.
Real memories retain the previous exact-source memory-read binding. No state
invariants, read consistency, implicit zero fill or out-of-range assumptions.
"""
import copy
import re
import subprocess
import hashlib
from collections import defaultdict
import event_scope_semantics as events
from event_scope_semantics import EventAdapter,EventBitVectors,lvalue_bases
from hierarchy_netlist_proof import NaturalNetlist
from real_parent_screen import replace
from slang_guard_adapter import Unsupported,walk
from spi_semantic_v2 import BitVectors
from natural_semantics import comb,statement

def expanded_instances(original):
    ast=copy.deepcopy(original);lookup={str(n['addr']):n for n in walk(ast) if 'addr' in n};notes=[];serial=0
    def expand(n):
        nonlocal serial
        if isinstance(n,list):
            for x in n:expand(x)
        elif isinstance(n,dict):
            if n.get('kind')=='Instance':
                if isinstance(n.get('body'),str):
                    serial+=1;body=copy.deepcopy(lookup[n['body'].split()[0]])
                    ids={str(x['addr']):'transaction'+str(serial)+'_'+str(x['addr']) for x in walk(body) if 'addr' in x}
                    def rename(x):
                        if isinstance(x,dict):return {k:(ids[str(v)] if k=='addr' and str(v) in ids else rename(v)) for k,v in x.items()}
                        if isinstance(x,list):return [rename(v) for v in x]
                        if isinstance(x,str) and ' ' in x and x.split(' ',1)[0] in ids:
                            a,b=x.split(' ',1);return ids[a]+' '+b
                        return x
                    n['body']=rename(body);lookup.update({str(x['addr']):x for x in walk(n['body']) if 'addr' in x})
                ports={p['name']:p for p in n['body']['members'] if p.get('kind')=='Port'}
                for c in n.get('connections',[]):
                    old=c['port'];p=ports[old['name']]
                    if old['direction']!=p['direction']:raise Unsupported('Cached instance port direction mismatch')
                    if old['internalSymbol']!=p['internalSymbol']:
                        notes.append({'instance_name':n['name'],'port':old['name'],'old':old['internalSymbol'],'new':p['internalSymbol'],
                                      'basis':'connection port rebound to same-name/direction member of its exact elaborated body; Yosys proof still required'})
                    c['port']=copy.deepcopy(p)
            for v in n.values():expand(v)
    expand(ast);return ast,notes

def bounds(t):
    a,b=map(int,re.fullmatch(r'\[(-?\d+):(-?\d+)\]',t['range']).groups())
    return min(a,b),max(a,b)

def slice_value(value,offset,info):
    if value['kind']=='Slice':offset+=value['offset'];value=value['value']
    return {'kind':'Slice','type':info,'value':value,'offset':offset}

def bounded_query(header,term,width,maximum,signed=False):
    if maximum<0:raise Unsupported('Negative select bound')
    invalid=[]
    if signed:invalid.append(f'(bvslt {term} {BitVectors.literal(0,width)})')
    if maximum < (1<<width):invalid.append(f'(bvugt {term} {BitVectors.literal(maximum,width)})')
    if not invalid:return {'z3':'unsat','basis':'entire unsigned bit-vector domain fits','maximum':maximum,'signed':signed}
    violation=invalid[0] if len(invalid)==1 else '(or '+' '.join(invalid)+')'
    query=header+f'\n(check-sat)\n(assert {violation})\n(check-sat)\n'
    p=subprocess.run(['z3','-in'],input=query,text=True,capture_output=True,timeout=10,check=True)
    if p.stdout.split()!=['sat','unsat']:raise Unsupported('Select range not independently proved: '+p.stdout.strip())
    return {'z3':'unsat','environment':'sat','maximum':maximum,'signed':signed,'smt2':query,'sha256':hashlib.sha256(query.encode()).hexdigest()}

class TransactionAdapter(EventAdapter):
    def __init__(self,ast,top,net):
        self.net=net;self.flat_wires=set(net['netnames']);self.array_bindings={}
        self.range_proofs={}
        ast,self.instance_rebinds=expanded_instances(ast)
        super().__init__(ast,top)

    def const(self,node):
        # Loop substitution can leave an evaluable Add/Multiply tree without
        # Slang's original constant annotation; no runtime expression allowed.
        return self.eval_constant(node)

    def prove_offset(self,node,offset,maximum):
        m=ExpressionOnly(self,expand_aliases=False);term=m.term(offset)
        header='(set-logic QF_BV)\n(set-option :timeout 1000)\n'+'\n'.join(f'(declare-fun {k} () (_ BitVec {v["type"]["width"]}))' for k,v in m.variables.items())
        key=hashlib.sha256((header+term+str(maximum)).encode()).hexdigest()
        if key not in self.range_proofs:self.range_proofs[key]={'source':self.source(node),**bounded_query(header,term,offset['type']['width'],maximum,offset['type']['signed'])}
        return key

    @staticmethod
    def scoped_read(node):
        if node['kind']=='MemoryRead':return {**node,'symbol':node['memory']+'::'+node['symbol']}
        return node

    def type_info(self,item):
        t=self.resolve(item)
        if t.get('kind')=='FixedSizeUnpackedArrayType':
            lo,hi=bounds(t);e=self.type_info(t['elementType'])
            if hi-lo+1>64:raise Unsupported('Unpacked wire array bound >64')
            return {'width':(hi-lo+1)*e['width'],'signed':False,'four_state':e['four_state']}
        return super().type_info(item)

    def typed(self,node):
        if node['kind']=='ElementSelect' and 'constant' not in node['selector']:
            try:i=self.const(node['selector'])
            except Unsupported:pass
            else:node={**node,'selector':{**node['selector'],'kind':'IntegerLiteral','constant':str(i),'value':str(i)}}
        if node['kind']=='RangeSelect':
            vt=self.resolve(node['value']['type']);info=self.type_info(node['type'])
            if vt['kind']=='PredefinedIntegerType':
                # SystemVerilog allows slices of int/logic integer values.
                right=self.const(node['right']);left=self.const(node['left'])
                offset={'Simple':right,'IndexedUp':left,'IndexedDown':left-right+1}[node['selectionKind']]
                value=self.typed(node['value'])
                if offset<0 or offset+info['width']>value['type']['width']:raise Unsupported('Integer slice bounds')
                return slice_value(value,offset,info)
            if node['selectionKind']=='IndexedUp':
                try:self.const(node['left'])
                except Unsupported:
                    if vt['kind']!='PackedArrayType' or bounds(vt)[0]!=0 or vt['range'].startswith('[0:'):raise Unsupported('Dynamic part-select layout: ascending packed index unsupported')
                    value=self.typed(node['value']);offset=self.typed(node['left'])
                    if self.const(node['right'])!=info['width']:raise Unsupported('Dynamic part-select size')
                    key=self.prove_offset(node,offset,value['type']['width']-info['width'])
                    return {'kind':'BoundedSlice','type':info,'value':value,'selector':offset,'range_proof':key}
        if node['kind']=='NamedValue' and self.resolve(node['type']).get('kind')=='FixedSizeUnpackedArrayType':
            name=node['symbol'].split(' ',1)[1]
            if name not in self.flat_wires:raise Unsupported('Unpacked storage is not a named flattened wire: '+name)
            self.array_bindings[name]={'symbol':name,'type':copy.deepcopy(self.resolve(node['type'])),'source':self.source(self.resolve(node['symbol'])),
                'layout':'rightmost declared unpacked index at lowest element offset; independently checked against Yosys, not a state invariant'}
        if node['kind']=='ElementSelect':
            vt=self.resolve(node['value']['type'])
            if vt.get('kind')=='PackedArrayType' and 'constant' not in node['selector']:
                info=self.type_info(node['type']);lo,hi=bounds(vt)
                if lo==0 and info['width']==1:
                    if vt['range'].startswith('[0:') and hi>0:raise Unsupported('Ascending dynamic packed bit-select unsupported')
                    value=self.typed(node['value']);offset=self.typed(node['selector'])
                    key=self.prove_offset(node,offset,hi)
                    return {'kind':'BoundedSlice','type':info,'value':value,'selector':offset,'range_proof':key}
            if vt.get('kind')=='FixedSizeUnpackedArrayType':
                # Preserve true-memory support; only named-wire arrays use a
                # packed view. Nested array values inherit that checked view.
                base=node['value']
                while base.get('kind')=='ElementSelect':base=base['value']
                if base.get('kind')!='NamedValue' or base['symbol'].split(' ',1)[1] not in self.flat_wires:
                    if base.get('kind')=='NamedValue' and 'constant' in node['selector']:
                        i=self.const(node['selector']);lo,hi=bounds(vt);src=self.source(node);name=base['symbol'].split(' ',1)[1]
                        if lo!=0 or not lo<=i<=hi:raise Unsupported('Memory constant index bounds')
                        location=f"{src['source']}:{src['line']}.{src['column']}-{src['end_line']}.{src['end_column']}"
                        cells=[c for c in self.net['cells'].values() if c['type']=='$memrd_v2' and c['parameters']['MEMID'].lstrip('\\')==name and c.get('attributes',{}).get('src')==location]
                        if len(cells)!=1:raise Unsupported('Constant memory read lacks exact source binding')
                        width=len(cells[0]['connections']['ADDR'])
                        if i>=1<<width:raise Unsupported('Memory constant address cannot fit')
                        sel={'kind':'constant','type':{'width':width,'signed':False,'four_state':True},'value':i}
                        return {'kind':'MemoryRead','type':self.type_info(node['type']),'selector':sel,'memory':name,'symbol':name+'::read@'+str(src),
                            'declaration':src,'source':src,'assumption':'arbitrary current read; fixed source/address verified; no memory state invariants'}
                    return self.scoped_read(super().typed(node))
                lo,hi=bounds(vt);left,right=map(int,re.fullmatch(r'\[(-?\d+):(-?\d+)\]',vt['range']).groups())
                info=self.type_info(node['type']);value=self.typed(node['value'])
                try:i=self.const(node['selector'])
                except Unsupported:
                    sel=self.typed(node['selector'])
                    if lo!=0 or hi+1!=1<<sel['type']['width'] or sel['type']['signed']:raise Unsupported('Unpacked wire selector domain not total')
                    if left<right:sel={'kind':'BinaryOp','op':'Subtract','type':sel['type'],'left':{'kind':'constant','type':sel['type'],'value':hi},'right':sel}
                    return {'kind':'TotalSelect','type':info,'value':value,'selector':sel,'elements':hi+1}
                if not lo<=i<=hi:raise Unsupported('Unpacked wire index out of bounds')
                return slice_value(value,(right-i if left<right else i-right)*info['width'],info)
        result=super().typed(node)
        if result['kind']=='Slice':return slice_value(result['value'],result['offset'],result['type'])
        return self.scoped_read(result)

    def extract(self):
        with replace(events,EventBitVectors=TransactionBitVectors):return super().extract()

class TransactionBitVectors(EventBitVectors):
    def term(self,node):
        if node['kind']=='BoundedSlice':
            w=node['type']['width'];vw=node['value']['type']['width'];sw=node['selector']['type']['width'];size=max(vw,sw)
            value=BitVectors.resize(self.term(node['value']),vw,size,False)
            selector=BitVectors.resize(self.term(node['selector']),sw,size,False)
            return f'((_ extract {w-1} 0) (bvlshr {value} {selector}))'
        return super().term(node)
    def _collect_procedures(self):
        pieces=defaultdict(list);clocked=set();saved=self.adapter.blocking_writes;self.adapter.blocking_writes=set()
        def bit(n,i):
            info={**n['type'],'width':1,'signed':False}
            if not any(x.get('kind')=='Uninitialized' for x in walk(n)):return slice_value(n,i,info)
            if n['kind']=='Insert':
                return bit(n['part'],i-n['offset']) if n['offset']<=i<n['offset']+n['part']['type']['width'] else bit(n['value'],i)
            if n['kind']=='Slice':return bit(n['value'],i+n['offset'])
            if n['kind']=='Concatenation':
                offset=0
                for operand in reversed(n['operands']):
                    if offset<=i<offset+operand['type']['width']:return bit(operand,i-offset)
                    offset+=operand['type']['width']
            if n['kind']=='ConditionalOp':
                a,b=bit(n['left'],i),bit(n['right'],i)
                if a is not None and b is not None:return {**n,'type':info,'left':a,'right':b}
            return None
        try:
            for p in self.adapter.body['members']:
                if p.get('kind')!='ProceduralBlock':continue
                body=statement(p)
                if not comb(p):
                    if p['procedureKind']!='Initial':
                        clocked.update(n['symbol'].split(' ',1)[1] for a in walk(body) if a.get('kind')=='Assignment' for n in lvalue_bases(a['left']))
                    continue
                try:
                    assigned={n['symbol']:self.adapter.typed(n) for a in walk(body) if a.get('kind')=='Assignment' for n in lvalue_bases(a['left'])}
                    initial={self.name(n):{'kind':'Uninitialized','type':n['type']} for n in assigned.values()}
                    final=self._statement(body,initial)
                    for n in assigned.values():
                        rhs=final[self.name(n)];parts={i:x for i in range(n['type']['width']) if (x:=bit(rhs,i)) is not None}
                        pieces[n['symbol']].append((n,parts,p))
                except Unsupported as e:self.unresolved.append({'source':self.adapter.source(p),'reason':str(e)})
            for name,rows in pieces.items():
                n=rows[0][0];key=self.name(n);bits={}
                try:
                    if name in clocked or key in self.definitions:raise Unsupported('Combinational/clocked or continuous co-driver')
                    for _,parts,p in rows:
                        if bits.keys() & parts.keys():raise Unsupported('Overlapping procedural bit writers')
                        bits.update(parts)
                    if set(bits)!=set(range(n['type']['width'])):raise Unsupported('Incomplete procedural bits; no latch/zero assumption')
                    rhs={'kind':'Concatenation','type':n['type'],'operands':[bits[i] for i in reversed(range(n['type']['width']))]}
                    self.definitions[key]=rhs;self.definition_sources[key]={'lhs':n,'rhs':rhs,'source':self.adapter.source(rows[0][2]),'source_parts':[self.adapter.source(p) for _,_,p in rows],
                        'method':'each combinational bit fully assigned on every path by one procedure; exact disjoint merge'}
                except Unsupported as e:self.unresolved.append({'signal':name,'reason':str(e)})
        finally:self.adapter.blocking_writes=saved

    def _collect_definitions(self):
        # Combine disjoint constant slices of one continuous wire. Every bit
        # must be assigned exactly once, and procedural co-drivers are rejected.
        by=defaultdict(list);blocked=set();procedural=set()
        for p in self.adapter.body['members']:
            if p.get('kind')=='ProceduralBlock':
                for a in walk(p):
                    if a.get('kind')=='Assignment':procedural.update(n['symbol'].split(' ',1)[1] for n in lvalue_bases(a['left']))
        def split(lhs,rhs,offset=0):
            if lhs['kind']=='Concatenation':
                result=[]
                for n in reversed(lhs['operands']):
                    result+=split(n,rhs,offset);offset+=self.adapter.type_info(n['type'])['width']
                return result
            lt=self.adapter.typed(lhs);w=lt['type']['width']
            rt=rhs if offset==0 and w==rhs['type']['width'] else slice_value(rhs,offset,lt['type'])
            if offset<0 or offset+w>rhs['type']['width']:raise Unsupported('Continuous slice sizing')
            base=lt['value'] if lt['kind']=='Slice' else lt
            if base['kind']!='NamedValue':raise Unsupported('Continuous destination is not a static wire slice')
            return [(base,lt.get('offset',0),rt)]
        for p in self.adapter.body['members']:
            if p.get('kind')!='ContinuousAssign':continue
            a=p['assignment']
            try:
                rhs=self.adapter.typed(a['right'])
                if self.adapter.type_info(a['left']['type'])['width']!=rhs['type']['width']:raise Unsupported('Continuous width mismatch')
                for lhs,offset,rhs in split(a['left'],rhs):by[lhs['symbol']].append((lhs,offset,rhs,p))
            except Unsupported as e:
                blocked.update(n['symbol'].split(' ',1)[1] for n in lvalue_bases(a['left']))
                self.unresolved.append({'source':self.adapter.source(p),'reason':str(e)})
        for name,parts in by.items():
            lhs=parts[0][0];key=self.name(lhs);rhs={'kind':'Uninitialized','type':lhs['type']};covered=set()
            if name in blocked or name in procedural:
                self.unresolved.append({'signal':name,'reason':'Unsupported or procedural co-driver'});continue
            try:
                for _,offset,part,p in parts:
                    mask=set(range(offset,offset+part['type']['width']))
                    if mask & covered or not mask<=set(range(lhs['type']['width'])):raise Unsupported('Overlapping/out-of-range continuous slices')
                    covered|=mask;rhs=self.packed_insert(rhs,part,offset,lhs['type'])
                if len(covered)!=lhs['type']['width']:raise Unsupported('Incomplete continuous wire; no zero fill')
                self.definitions[key]=rhs;self.definition_sources[key]={'lhs':lhs,'rhs':rhs,'source':self.adapter.source(parts[0][3]),
                    'source_parts':[self.adapter.source(p) for _,_,_,p in parts],'method':'disjoint exact continuous slices, all bits assigned'}
            except Unsupported as e:self.unresolved.append({'signal':name,'reason':str(e)})

class ObservationNetlist(NaturalNetlist):
    evidence=[]
    def __init__(self,module):
        view=copy.deepcopy(module);self.omitted_observers=[]
        for key,c in list(view['cells'].items()):
            if c['type']=='$print':
                if any(x!='input' for x in c['port_directions'].values()):raise Unsupported('Print cell drives a net')
                self.omitted_observers.append({'cell':key,'type':'$print','basis':'input-only observation has no driven RTL net'})
                del view['cells'][key]
        super().__init__(view)

    def cell(self,name):
        c=self.module['cells'][name]
        if c['type']!='$shiftx':return super().cell(name)
        p=c['connections'];aw,bw,w=len(p['A']),len(p['B']),len(p['Y']);key='n_'+hashlib.sha256(name.encode()).hexdigest()[:20]
        if key in self.macros:return key,w
        if name in self.active:raise Unsupported('Combinational cycle')
        self.active.add(name)
        try:
            b=self.word(p['B']);a=self.word(p['A'])
            decl='\n'.join(f'(declare-fun b{x} () (_ BitVec 1))' for x in sorted(self.primary) if isinstance(x,int))
            decl+='\n'+'\n'.join(f'(declare-fun {x} () (_ BitVec 1))' for x in self.unknown_bits)
            header='(set-logic QF_BV)\n(set-option :timeout 1000)\n'+decl+'\n'+'\n'.join(self.macros.values())
            proof=bounded_query(header,b,bw,aw-w,bool(int(c['parameters']['B_SIGNED'],2)));self.evidence.append({'cell':name,**proof})
            size=max(aw,bw);expr=f'(bvlshr {BitVectors.resize(a,aw,size,False)} {BitVectors.resize(b,bw,size,False)})'
            expr=BitVectors.resize(expr,size,w,False);self.macros[key]=f'(define-fun {key} () (_ BitVec {w}) {expr})';self.used_cells.add(name)
            return key,w
        finally:self.active.remove(name)

class ExpressionOnly(TransactionBitVectors):
    def _collect_definitions(self):pass
