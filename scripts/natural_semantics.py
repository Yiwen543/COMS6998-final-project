"""Typed static semantics for natural-IP screening; old frozen adapters unchanged.

Two-state only. Whole-process SSA is used for combinational output definitions;
predicate atoms use the SSA environment at their actual statement position.
Clocked processes retain lexical edge/reset context; no state invariant inferred.
"""
import copy
import re
from contextlib import contextmanager
from slang_guard_adapter import walk,both,any_of,Unsupported
from spi_semantic_v2 import RichAdapter,BitVectors,integer


def comb(proc):
    b=proc['body']
    return proc['procedureKind']=='AlwaysComb' or (proc['procedureKind']=='Always' and
        b.get('kind')=='Timed' and b.get('timing',{}).get('kind')=='ImplicitEvent')


def statement(proc):
    b=proc['body'];return b['stmt'] if b.get('kind')=='Timed' and comb(proc) else b


class NaturalAdapter(RichAdapter):
    def __init__(self,ast,top):
        super().__init__(ast,top);self.environment=None;self.procedure_notes=[]

    def add(self,node,guard,context,depth,outcome,predicate=None,anchor=None):
        super().add(node,guard,context,depth,outcome,predicate,anchor)
        if predicate is not None and outcome!='case':
            self.targets[-1]['local_compact']=self.boolean(predicate)
        else:self.targets[-1]['local_compact']=None

    @contextmanager
    def scope(self,env):
        prior=self.environment;self.environment=env
        try:yield
        finally:self.environment=prior

    def const(self,node):
        if 'constant' not in node:raise Unsupported('Nonconstant slice/count')
        info=self.type_info(node['type']);v=integer(node['constant'],info['width'])
        return v-(1<<info['width']) if info['signed'] and v&(1<<(info['width']-1)) else v

    def typed(self,node):
        kind=node['kind']
        if kind=='ElementSelect':
            info=self.type_info(node['type']);v=self.resolve(node['value']['type'])
            if v['kind']!='PackedArrayType':raise Unsupported('Element select of non-packed value')
            ends=re.fullmatch(r'\[(-?\d+):(-?\d+)\]',v['range']);hi,lo=map(int,ends.groups())
            if hi<lo:raise Unsupported('Ascending packed index not implemented')
            i=self.const(node['selector']);ew=self.type_info(v['elementType'])['width']
            if not lo<=i<=hi or ew!=info['width']:raise Unsupported('Out-of-range or mismatched packed element select')
            result={'kind':'Slice','type':info,'value':self.typed(node['value']),'offset':(i-lo)*ew}
        elif kind in ('Concatenation','Replication','RangeSelect'):
            info=self.type_info(node['type'])
            if kind=='Concatenation':
                result={'kind':kind,'type':info,'operands':[self.typed(n) for n in node['operands']]}
            elif kind=='Replication':
                result={'kind':kind,'type':info,'count':self.const(node['count']),'value':self.typed(node['concat'])}
            else:
                v=self.resolve(node['value']['type'])
                if v['kind']!='PackedArrayType' or self.type_info(v['elementType'])['width']!=1:
                    raise Unsupported('Slice of non-flat packed array')
                ends=re.fullmatch(r'\[(-?\d+):(-?\d+)\]',v['range']);hi,lo=map(int,ends.groups())
                if hi<lo:raise Unsupported('Ascending slice layout not implemented')
                left,right=self.const(node['left']),self.const(node['right'])
                low={'Simple':right,'IndexedUp':left,'IndexedDown':left-right+1}.get(node['selectionKind'])
                if low is None or low<lo or low+info['width']-1>hi:raise Unsupported('Slice out of range')
                result={'kind':'Slice','type':info,'value':self.typed(node['value']),'offset':low-lo}
        else:result=super().typed(node)
        if result['kind']=='NamedValue' and self.environment is not None:
            return self.environment.get(BitVectors.name(result),result)
        return result

    def visit(self,node,guard,context,depth=0):
        # RichAdapter recursively calls this entry. Each branch gets its own
        # incoming SSA environment, then the ordered join updates the parent.
        if self.environment is None or not isinstance(node,dict):
            return super().visit(node,guard,context,depth)
        kind=node.get('kind');env=self.environment
        if kind in ('Block','List'):
            items=[node['body']] if kind=='Block' else node['list']
            for child in items:
                with self.scope(env):self.visit(child,guard,context,depth)
                env=self.ssa._statement(child,env)
            return
        if kind=='Conditional':
            # Parent visitor establishes exact branch polarity/source anchors;
            # recursive calls do not leak assignment state to siblings.
            return super().visit(node,guard,context,depth)
        if kind=='Case':return super().visit(node,guard,context,depth)
        return super().visit(node,guard,context,depth)

    def extract(self):
        self.ssa=NaturalBitVectors(self,procedural=False)
        members=self.body['members']
        try:
            for p in members:
                if p.get('kind')=='ProceduralBlock' and comb(p):
                    self.blocking_writes=set()
                    assigned={n['symbol']:self.typed(n) for a in walk(statement(p))
                        if a.get('kind')=='Assignment' for n in walk(a['left']) if n.get('kind')=='NamedValue'}
                    env={BitVectors.name(n):{'kind':'Uninitialized','type':n['type']} for n in assigned.values()}
                    before=len(self.targets)
                    try:
                        with self.scope(env):self.visit(statement(p),'true',['combinational'],0)
                    except Unsupported as e:
                        del self.targets[before:]
                        self.unsupported.append({**self.source(p),'reason':str(e),'descendants':'whole procedure withheld'})
                    self.procedure_notes.append({**self.source(p),'original_kind':p['procedureKind'],
                        'implicit_all':p['body'].get('timing',{}).get('kind')=='ImplicitEvent',
                        'scope':'static blocking-SSA analysis only; no always_comb scheduling substitution'})
                else:
                    self.body['members']=[p];super().extract()
        finally:self.body['members']=members;self.environment=None;self.blocking_writes=set()
        return self


class NaturalBitVectors(BitVectors):
    def _collect_procedures(self):
        # The inherited collector needs only its selection/body view changed;
        # original AST and procedure timing metadata are restored immediately.
        original=self.adapter.body['members'];view=[]
        for p in original:
            if p.get('kind')=='ProceduralBlock' and comb(p):
                view.append({**p,'procedureKind':'AlwaysComb','body':statement(p)})
            else:view.append(p)
        self.adapter.body['members']=view
        try:super()._collect_procedures()
        finally:self.adapter.body['members']=original

    def _statement(self,node,env):
        env=dict(env)
        # SSA expression translation must not apply the visitor environment twice.
        with self.adapter.scope(None):
            if node and node.get('kind')=='ExpressionStatement':
                a=node['expr']
                if a.get('kind')=='Assignment' and not a.get('isNonBlocking') and a['left']['kind']=='MemberAccess':
                    lhs=self.adapter.typed(a['left']);base=self.adapter.typed(a['left']['value'])
                    if base['kind']!='NamedValue':raise Unsupported('Nested/indirect partial assignment')
                    key=self.name(base);rhs=self._expression(a['right'],env)
                    env[key]={'kind':'Insert','type':base['type'],'value':env[key],'part':rhs,'offset':lhs['bit_offset']}
                    return env
            return super()._statement(node,env)

    def term(self,node):
        k=node['kind'];w=node['type']['width']
        if k=='UnaryOp' and node['op'] in ('BitwiseNor','BitwiseNand','BitwiseXor','BitwiseXnor'):
            a=node['operand'];aw=a['type']['width'];t=self.term(a)
            if node['op']=='BitwiseNor':return self.bit(f'(= {t} {self.literal(0,aw)})')
            if node['op']=='BitwiseNand':return self.bit(f'(not (= {t} {self.literal((1<<aw)-1,aw)}))')
            bits=[f'((_ extract {i} {i}) {t})' for i in range(aw)];s=bits[0]
            for bit in bits[1:]:s=f'(bvxor {s} {bit})'
            return f'(bvnot {s})' if node['op']=='BitwiseXnor' else s
        if k=='BinaryOp' and node['op'] in ('LogicalShiftLeft','LogicalShiftRight','ArithmeticShiftLeft','ArithmeticShiftRight'):
            l,r=node['left'],node['right'];lw,rw=l['type']['width'],r['type']['width']
            if lw!=w:raise Unsupported('Shift operand sizing not elaborated')
            size=max(w,rw);signed=node['op']=='ArithmeticShiftRight' and l['type']['signed']
            a=self.resize(self.term(l),w,size,signed);b=self.resize(self.term(r),rw,size,False)
            op='bvashr' if signed else ('bvshl' if node['op'].endswith('Left') else 'bvlshr')
            return self.resize(f'({op} {a} {b})',size,w,False)
        if k in ('Concatenation','Replication'):
            parts=node['operands'] if k=='Concatenation' else [node['value']]*node['count']
            if not parts or sum(x['type']['width'] for x in parts)!=w:raise Unsupported('Concat/replication width mismatch')
            terms=[self.term(x) for x in parts];s=terms[0]
            for t in terms[1:]:s=f'(concat {s} {t})'
            return s
        if k=='Slice':
            o=node['offset'];vw=node['value']['type']['width']
            if o<0 or o+w>vw:raise Unsupported('Invalid slice')
            return f'((_ extract {o+w-1} {o}) {self.term(node["value"])})'
        if k=='Insert':
            o=node['offset'];pw=node['part']['type']['width']
            if o<0 or o+pw>w:raise Unsupported('Invalid packed field update')
            mask=((1<<pw)-1)<<o
            old=self.term(node['value']);part=self.resize(self.term(node['part']),pw,w,False)
            return f'(bvor (bvand {old} {self.literal(((1<<w)-1)^mask,w)}) (bvshl {part} {self.literal(o,w)}))'
        return super().term(node)
