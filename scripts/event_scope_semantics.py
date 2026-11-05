"""New-scope constant elaboration view; never edits frozen adapters or RTL.

Slang supplies parameter-evaluated condition values. A statically false branch
is withheld with provenance, not assumed dynamically unreachable. Its original
Verilator counters remain in the denominator. Independent Yosys checking still
must certify all definitions before any feedback group is admitted.
"""
import copy
from real_parent_semantics import ParentAdapter,ParentBitVectors
from spi_semantic_v2 import integer,BitVectors,RichAdapter
from slang_guard_adapter import walk,Unsupported
from natural_semantics import comb,statement

def lvalue_bases(node):
    """Only storage written: indices/range parameters are reads, never writers."""
    k=node['kind']
    if k=='NamedValue':return [node]
    if k in ('ElementSelect','RangeSelect','MemberAccess'):return lvalue_bases(node['value'])
    if k=='Concatenation':return [n for x in node['operands'] for n in lvalue_bases(x)]
    raise Unsupported('Unsupported assignment destination: '+k)

class EventAdapter(ParentAdapter):
    def eval_constant(self,node,bindings=None):
        # Slang can emit literal `value` without `constant` inside static loops.
        # Apply the elaborated width/sign after every supported operation.
        k=node['kind'];info=self.type_info(node['type']);w=info['width']
        if k=='IntegerLiteral' and 'constant' not in node:
            value=integer(node['value'],w)
        elif k=='UnaryOp' and 'constant' not in node and node['op']=='Minus':
            value=-self.eval_constant(node['operand'],bindings)
        elif k=='BinaryOp' and 'constant' not in node and node['op'] in ('LessThanEqual','GreaterThan','Multiply'):
            a=self.eval_constant(node['left'],bindings);b=self.eval_constant(node['right'],bindings)
            value={'LessThanEqual':lambda:int(a<=b),'GreaterThan':lambda:int(a>b),'Multiply':lambda:a*b}[node['op']]()
        else:return super().eval_constant(node,bindings)
        value%=1<<w
        return value-(1<<w) if info['signed'] and value&(1<<(w-1)) else value

    def __init__(self,ast,top):
        super().__init__(ast,top)
        self.constant_branch_elaboration=[]
        def fold(node):
            if isinstance(node,list):return [fold(n) for n in node]
            if not isinstance(node,dict):return node
            if node.get('kind')=='Conditional' and len(node.get('conditions',[]))==1:
                condition=node['conditions'][0].get('expr',{})
                if 'constant' in condition:
                    try:
                        info=self.type_info(condition['type']);value=integer(condition['constant'],info['width'])
                    except (ValueError,KeyError):pass
                    else:
                        self.constant_branch_elaboration.append({**self.source(node),'condition':self.text(condition),'constant':condition['constant'],
                            'selected':'ifTrue' if value else 'ifFalse','basis':'Slang elaborated constant; no runtime state or reachability assumption'})
                        return fold(node.get('ifTrue' if value else 'ifFalse',{'kind':'Empty'}))
            return {k:fold(v) for k,v in node.items()}
        self.body['members']=fold(copy.deepcopy(self.body['members']))

    def unroll(self,node):
        if isinstance(node,list):return [self.unroll(x) for x in node]
        if not isinstance(node,dict):return node
        if node.get('kind')!='ForLoop':return {k:self.unroll(v) for k,v in node.items()}
        try:
            if len(node['initializers'])!=1 or len(node['steps'])!=1:raise Unsupported('Multiple loop variables')
            init,step=node['initializers'][0],node['steps'][0]
            if any(x.get('kind')!='Assignment' or x['left']['kind']!='NamedValue' for x in (init,step)):raise Unsupported('Loop syntax')
            key=init['left']['symbol']
            if step['left']['symbol']!=key:raise Unsupported('Loop step mismatch')
            if any(n.get('kind')=='Assignment' and any(x['symbol']==key for x in lvalue_bases(n['left'])) for n in walk(node['body'])):
                raise Unsupported('Loop body actually writes induction variable')
            value=self.eval_constant(init['right']);items=[];values=[]
            def substitute(n,v):
                if isinstance(n,dict):
                    if n.get('kind')=='NamedValue' and n.get('symbol')==key:return {**n,'kind':'IntegerLiteral','value':str(v),'constant':str(v)}
                    return {k:substitute(x,v) for k,x in n.items()}
                if isinstance(n,list):return [substitute(x,v) for x in n]
                return n
            while self.eval_constant(node['stopExpr'],{key:value}):
                if len(values)>=64:raise Unsupported('Static loop bound exceeds64')
                values.append(value);items.append(self.unroll(substitute(node['body'],value)))
                value=self.eval_constant(step['right'],{key:value})
            right={**init['left'],'kind':'IntegerLiteral','constant':str(value),'value':str(value)}
            items.append({'kind':'ExpressionStatement','expr':{**init,'right':right},**{k:v for k,v in node.items() if k.startswith('source_')}})
            self.loop_unrolls.append({**self.source(node),'values':values,'final_value':value,'bound':64})
            return {**node,'kind':'List','list':items,'_unrolled_loop':True}
        except Unsupported as e:
            self.unsupported.append({**self.source(node),'reason':str(e),'scope':'loop withheld'});return node

    def extract(self):
        self.ssa=EventBitVectors(self,procedural=False);members=self.body['members']
        try:
            for p in members:
                if p.get('_port_alias'):continue
                self.current_hierarchy=p.get('_hierarchy','')
                if p.get('kind')=='ProceduralBlock' and comb(p):
                    self.blocking_writes=set();body=statement(p);before=len(self.targets)
                    try:
                        assigned={n['symbol']:self.typed(n) for a in walk(body) if a.get('kind')=='Assignment' for n in lvalue_bases(a['left'])}
                        env={BitVectors.name(n):{'kind':'Uninitialized','type':n['type']} for n in assigned.values()}
                        with self.scope(env):self.visit(body,'true',['combinational'],0)
                    except Unsupported as e:
                        del self.targets[before:];self.unsupported.append({**self.source(p),'reason':str(e),'descendants':'whole procedure withheld','instance_scope':self.current_hierarchy})
                    self.procedure_notes.append({**self.source(p),'instance_scope':self.current_hierarchy,'original_kind':p['procedureKind'],'scope':'statement-position blocking SSA with exact assignment destinations'})
                else:
                    self.body['members']=[p];RichAdapter.extract(self)
        finally:self.body['members']=members;self.environment=None;self.blocking_writes=set()
        return self

class EventBitVectors(ParentBitVectors):
    def _collect_procedures(self):
        procedures=[p for p in self.adapter.body['members'] if p.get('kind')=='ProceduralBlock'];owners={}
        for i,p in enumerate(procedures):
            for a in walk(p):
                if a.get('kind')=='Assignment':
                    for n in lvalue_bases(a['left']):owners.setdefault(n['symbol'],set()).add(i)
        saved=self.adapter.blocking_writes;self.adapter.blocking_writes=set()
        try:
            for i,p in enumerate(procedures):
                if not comb(p):continue
                body=statement(p)
                try:
                    assigned={n['symbol']:self.adapter.typed(n) for a in walk(body) if a.get('kind')=='Assignment' for n in lvalue_bases(a['left'])}
                    if any(len(owners[s])!=1 for s in assigned):raise Unsupported('Multiple procedural writers')
                    initial={self.name(n):{'kind':'Uninitialized','type':n['type']} for n in assigned.values()}
                    final=self._statement(body,initial)
                    for n in assigned.values():
                        key=self.name(n);rhs=final[key]
                        if any(x.get('kind')=='Uninitialized' for x in walk(rhs)):
                            self.unresolved.append({'source':self.adapter.source(p),'signal':n['symbol'],'reason':'Not assigned on every path; no latch assumption allowed'});continue
                        if key in self.definitions:raise Unsupported('Procedural and continuous multiple drivers')
                        self.definitions[key]=rhs;self.definition_sources[key]={'lhs':n,'rhs':rhs,'source':self.adapter.source(p),
                            'source_text':self.adapter.text(body),'method':'blocking SSA with exact lvalue ownership; full ordered if/case'}
                except Unsupported as e:self.unresolved.append({'source':self.adapter.source(p),'reason':str(e)})
        finally:self.adapter.blocking_writes=saved
