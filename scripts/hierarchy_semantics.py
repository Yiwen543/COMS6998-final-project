"""Instance-qualified, source-preserving two-state semantic view.

Original AST/RTL stay untouched. Connections become typed directed definitions,
not name-based unions. Every definition must subsequently pass the independent
Yosys-cell proof. Elaboration-time generate blocks add scope, not dynamic guards.
"""
import copy
import re
from collections import defaultdict
from natural_semantics import NaturalAdapter,NaturalBitVectors,comb,statement
from slang_guard_adapter import walk,Unsupported
from spi_semantic_v2 import BitVectors,integer


def hierarchical_view(original,top):
    ast=copy.deepcopy(original)
    lookup={str(n['addr']):n for n in walk(ast) if 'addr' in n};serial=0
    def expand(n):
        nonlocal serial
        if isinstance(n,list):
            for x in n:expand(x)
        elif isinstance(n,dict):
            if n.get('kind')=='Instance' and isinstance(n.get('body'),str):
                ref=n['body'].split()[0]
                if ref not in lookup:raise Unsupported('Missing cached instance body')
                body=copy.deepcopy(lookup[ref]);serial+=1
                ids={str(x['addr']):'instance'+str(serial)+'_'+str(x['addr']) for x in walk(body) if 'addr' in x}
                def rename(x):
                    if isinstance(x,dict):
                        return {k:(ids[str(v)] if k=='addr' and str(v) in ids else rename(v)) for k,v in x.items()}
                    if isinstance(x,list):return [rename(v) for v in x]
                    if isinstance(x,str) and ' ' in x and x.split(' ',1)[0] in ids:
                        first,rest=x.split(' ',1);return ids[first]+' '+rest
                    return x
                n['body']=rename(body);n['connections']=rename(n['connections'])
                lookup.update({str(x['addr']):x for x in walk(n['body']) if 'addr' in x})
            for v in n.values():expand(v)
    expand(ast)
    inst=next(n for n in walk(ast) if n.get('kind')=='Instance' and n.get('name')==top)
    names={};members=[];connections=[];instances=[];notes=[]
    def collect(body,path):
        for m in body.get('members',[]):
            k=m.get('kind')
            if k=='Instance':
                child=path+[m['name']];instances.append({'path':'.'.join(child),'definition':m['body'].get('definition'),'source':{k:v for k,v in m.items() if k.startswith('source_')}})
                connections.extend((child,c,m) for c in m['connections']);collect(m['body'],child)
            elif k=='GenerateBlockArray':
                for b in m['members']:
                    if b.get('kind')!='GenerateBlock' or b.get('isUninstantiated'):continue
                    indices=[x['value'] for x in b['members'] if x.get('kind')=='Parameter' and x['name']==m['loopVariable'].split(' ',1)[-1]]
                    if len(indices)!=1:raise Unsupported('Missing elaborated generate index')
                    collect(b,path+[m['name']+'['+str(indices[0])+']'])
            elif k=='GenerateBlock':
                if m.get('isUninstantiated'):continue
                if not m.get('name'):raise Unsupported('Unnamed generate scope needs explicit netlist match')
                collect(m,path+[m['name']])
            else:
                if k in ('Net','Variable','Parameter','Port','TypeAlias','EnumValue') and 'addr' in m:
                    names[str(m['addr'])]='.'.join(path+[m['name']])
                # Process locals must also be distinct in reused instances.
                if k=='ProceduralBlock':
                    for d in walk(m):
                        if d.get('kind') in ('Variable','Net') and 'addr' in d:
                            names.setdefault(str(d['addr']),'.'.join(path+[d['name']]))
                m['_hierarchy']='.'.join(path);members.append(m)
    collect(inst['body'],[])
    # Rename references by elaborated declaration identity. Source identity alone
    # is insufficient for multiple instances of the same module.
    for n in walk(ast):
        for key in ('symbol','internalSymbol'):
            ref=n.get(key)
            if isinstance(ref,str) and ref.split()[0] in names:
                n[key]=ref.split()[0]+' '+names[ref.split()[0]]
    for path,c,parent in connections:
        port=c['port'];expr=c.get('expr');ref=port['internalSymbol']
        src={k:v for k,v in parent.items() if k.startswith('source_')}
        node={'kind':'NamedValue','symbol':ref,'type':port['type'],**src}
        note={'instance':'.'.join(path),'port':port['name'],'direction':port['direction'],'source':src}
        if expr is None:note['status']='unconnected';notes.append(note);continue
        if port['direction']=='In':left,right=node,expr
        elif port['direction']=='Out' and expr.get('kind')=='Assignment':
            def replace(n):
                if isinstance(n,dict):
                    if n.get('kind')=='EmptyArgument':return node
                    return {k:replace(v) for k,v in n.items()}
                if isinstance(n,list):return [replace(x) for x in n]
                return n
            left,right=expr['left'],replace(expr['right'])
        else:raise Unsupported('Unproved inout/ref/output connection')
        assignment={'kind':'Assignment','type':left['type'],'left':left,'right':right,'isNonBlocking':False,**src}
        members.append({'kind':'ContinuousAssign','assignment':assignment,**src,'_hierarchy':'.'.join(path[:-1]),'_port_alias':True})
        note.update(status='requires_netlist_proof',internal_symbol=ref.split(' ',1)[1],expression_kind=expr['kind']);notes.append(note)
    # Keep original type/package index separately, including declarations no
    # longer reachable through the flattened member list.
    index={str(n['addr']):n for n in walk(ast) if 'addr' in n}
    inst['body']['members']=members
    return ast,index,notes,instances


class HierarchyAdapter(NaturalAdapter):
    def __init__(self,ast,top):
        view,index,aliases,instances=hierarchical_view(ast,top)
        super().__init__(view,top);self.index.update(index)
        self.port_aliases=aliases;self.instances=instances;self.current_hierarchy='';self.function_bindings={};self.function_stack=[]
        self.type_alias_repairs=[];self.loop_unrolls=[]
        # Slang omits a TypeAlias record for elaborated type parameters. Resolve
        # only a unique package/module-qualified parameter, retaining evidence.
        parameters=defaultdict(list)
        for n in walk(view):
            if n.get('kind')=='Instance':
                module=n['body']['definition'].split(' ',1)[-1]
                for x in n['body']['members']:
                    if x.get('kind')=='TypeParameter':parameters[module+'.'+x['name']].append(x)
        # Flattening removes children from view; original AST provides ownership.
        for n in self.index.values():
            if n.get('kind')=='Instance' and isinstance(n.get('body'),dict):
                module=n['body']['definition'].split(' ',1)[-1]
                for x in n['body']['members']:
                    if x.get('kind')=='TypeParameter':parameters[module+'.'+x['name']].append(x)
        for n in list(self.index.values()):
            for x in walk(n):
                ref=x.get('type')
                if isinstance(ref,str) and ref.split()[0] not in self.index:
                    candidates=parameters.get(ref.split(' ',1)[-1],[])
                    types={str(c['type']) for c in candidates}
                    if len(types)==1:
                        self.index[ref.split()[0]]={'kind':'TypeAlias','target':candidates[0]['type']}
                        self.type_alias_repairs.append({'reference':ref.split(' ',1)[-1],'type_parameter':candidates[0]['name'],'actual_type':candidates[0]['type']})
        self.body['members']=[self.unroll(p) for p in self.body['members']]

    def typed(self,node):
        if node['kind']=='NamedValue' and node['symbol'].split()[0] in self.function_bindings:
            return self.function_bindings[node['symbol'].split()[0]]
        if node['kind']=='Call':
            if 'constant' in node:
                info=self.type_info(node['type']);return {'kind':'constant','type':info,'value':integer(node['constant'],info['width'])}
            if node.get('subroutine') in ('$signed','$unsigned'):return super().typed(node)
            f=self.resolve(node['subroutine']);args=f.get('arguments',[])
            if f.get('subroutineKind')!='Function' or f['body'].get('kind')!='Return' or any(a['direction']!='In' for a in args):
                raise Unsupported('Only pure single-return functions supported')
            if len(args)!=len(node['arguments']) or f['addr'] in self.function_stack:raise Unsupported('Recursive/arity-mismatched call')
            actual=[self.typed(x) for x in node['arguments']];old=self.function_bindings
            for a,b in zip(args,actual):
                if self.type_info(a['type'])['width']!=b['type']['width']:raise Unsupported('Unelaborated argument sizing')
            self.function_bindings={**old,**{str(a['addr']):b for a,b in zip(args,actual)}};self.function_stack.append(f['addr'])
            try:result=self.typed(f['body']['expr'])
            finally:self.function_bindings=old;self.function_stack.pop()
            if result['type']['width']!=self.type_info(node['type'])['width']:raise Unsupported('Unelaborated return sizing')
            return result
        if node['kind']=='ElementSelect' and 'constant' not in node['selector']:
            v=self.resolve(node['value']['type']);s=self.typed(node['selector']);info=self.type_info(node['type'])
            if v.get('kind')=='FixedSizeUnpackedArrayType' and node['value']['kind']=='NamedValue':
                # One free current read value per source expression. No memory
                # consistency or sequential invariant is invented.
                mem=self.resolve(node['value']['symbol']);src=self.source(node)
                hi,lo=map(int,re.fullmatch(r'\[(-?\d+):(-?\d+)\]',v['range']).groups())
                if min(hi,lo)!=0 or max(hi,lo)+1!=1<<s['type']['width'] or s['type']['signed']:
                    raise Unsupported('Unpacked read index is not total')
                return {'kind':'MemoryRead','type':info,'selector':s,'memory':node['value']['symbol'].split(' ',1)[1],
                    'symbol':'read@'+str(src),'declaration':src,'source':src,'assumption':'arbitrary current read, no memory invariants'}
            if s['kind']=='constant':
                clone={**node,'selector':{**node['selector'],'constant':str(s['value'])}};return super().typed(clone)
            if v.get('kind')!='PackedArrayType':raise Unsupported('Dynamic unpacked/memory read not translated')
            hi,lo=map(int,re.fullmatch(r'\[(-?\d+):(-?\d+)\]',v['range']).groups())
            if lo!=0 or hi+1!=1<<s['type']['width'] or s['type']['signed']:
                raise Unsupported('Dynamic index not total over binary selector domain')
            ew=self.type_info(v['elementType'])['width']
            if ew!=info['width']:raise Unsupported('Packed select width mismatch')
            return {'kind':'TotalSelect','type':info,'value':self.typed(node['value']),'selector':s,'elements':hi+1}
        if node['kind']=='BinaryOp' and node['op']=='Power':
            info=self.type_info(node['type']);value=self.eval_constant(node)
            return {'kind':'constant','type':info,'value':value%(1<<info['width'])}
        return super().typed(node)

    def eval_constant(self,node,bindings=None):
        bindings=bindings or {};k=node['kind'];info=self.type_info(node['type']);w=info['width']
        if k=='NamedValue' and node['symbol'] in bindings:value=bindings[node['symbol']]
        elif 'constant' in node:value=integer(node['constant'],w)
        elif k=='NamedValue':
            n=self.resolve(node['symbol'])
            if n['kind'] not in ('Parameter','EnumValue','LocalParameter'):raise Unsupported('Nonconstant loop/power expression')
            value=integer(n.get('value',n.get('initializer',{}).get('constant')),w)
        elif k=='Conversion':value=self.eval_constant(node['operand'],bindings)
        elif k=='BinaryOp':
            a=self.eval_constant(node['left'],bindings);b=self.eval_constant(node['right'],bindings)
            op=node['op']
            if op=='Power':
                if b<0 or b>1024:raise Unsupported('Unbounded power')
                value=pow(a,b,1<<w)
            elif op=='Add':value=a+b
            elif op=='Subtract':value=a-b
            elif op=='LessThan':value=int(a<b)
            elif op=='GreaterThanEqual':value=int(a>=b)
            else:raise Unsupported('Unsupported constant evaluator '+op)
        else:raise Unsupported('Unsupported constant expression '+k)
        value%=1<<w
        return value-(1<<w) if info['signed'] and value&(1<<(w-1)) else value

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
            if any(n.get('kind')=='Assignment' and any(x.get('symbol')==key for x in walk(n['left'])) for n in walk(node['body'])):raise Unsupported('Loop body changes induction variable')
            value=self.eval_constant(init['right']);items=[];values=[]
            def substitute(n,v):
                if isinstance(n,dict):
                    if n.get('kind')=='NamedValue' and n.get('symbol')==key:
                        return {**n,'kind':'IntegerLiteral','value':str(v),'constant':str(v)}
                    return {k:substitute(x,v) for k,x in n.items()}
                if isinstance(n,list):return [substitute(x,v) for x in n]
                return n
            while self.eval_constant(node['stopExpr'],{key:value}):
                if len(values)>=64:raise Unsupported('Static loop bound exceeds64')
                values.append(value);items.append(self.unroll(substitute(node['body'],value)))
                value=self.eval_constant(step['right'],{key:value})
            # Retain the induction variable's final assignment. It may be a
            # latch outside this conditional path and is never assumed zero.
            right={**init['left'],'kind':'IntegerLiteral','constant':str(value),'value':str(value)}
            items.append({'kind':'ExpressionStatement','expr':{**init,'right':right},**{k:v for k,v in node.items() if k.startswith('source_')}})
            self.loop_unrolls.append({**self.source(node),'values':values,'final_value':value,'bound':64})
            return {**node,'kind':'List','list':items,'_unrolled_loop':True}
        except Unsupported as e:
            self.unsupported.append({**self.source(node),'reason':str(e),'scope':'loop withheld'})
            return node

    def add(self,node,guard,context,depth,outcome,predicate=None,anchor=None):
        super().add(node,guard,context,depth,outcome,predicate,anchor)
        target=self.targets[-1];target['instance_scope']=self.current_hierarchy
        if outcome!='cond_then' or anchor is None:return
        while anchor.get('kind')=='Conversion':anchor=anchor['operand']
        if anchor['kind']=='ElementSelect':
            value=self.source(anchor['value']);selector=self.source(anchor['selector'])
            if value['end_line']!=selector['line']:return
            from run_midterm_fixed import ROOT
            line=(ROOT/value['source']).read_text().splitlines()[value['end_line']-1]
            middle=line[value['end_column']-1:selector['column']-1]
            if middle.strip()!='[':return
            column=value['end_column']+len(middle)-len(middle.lstrip())
            target['counter_anchor']={**target['counter_anchor'],'line':value['end_line'],'column':column}
            target['counter_anchor_basis']='AST packed-select opening bracket token, verified between value/selector spans'
        elif anchor['kind']=='Replication':
            src=self.source(anchor['concat'])
            if not self.text(anchor['concat']).startswith('{'):return
            target['counter_anchor']=src;target['counter_anchor_basis']='AST replication inner concatenation opening brace token'


    def extract(self):
        self.ssa=HierarchyBitVectors(self,procedural=False);members=self.body['members']
        try:
            for p in members:
                if p.get('_port_alias'):continue
                self.current_hierarchy=p.get('_hierarchy','')
                if p.get('kind')=='ProceduralBlock' and comb(p):
                    self.blocking_writes=set();body=statement(p)
                    assigned={n['symbol']:self.typed(n) for a in walk(body) if a.get('kind')=='Assignment' for n in walk(a['left']) if n.get('kind')=='NamedValue'}
                    env={BitVectors.name(n):{'kind':'Uninitialized','type':n['type']} for n in assigned.values()};before=len(self.targets)
                    try:
                        with self.scope(env):self.visit(body,'true',['combinational'],0)
                    except Unsupported as e:
                        del self.targets[before:];self.unsupported.append({**self.source(p),'reason':str(e),'descendants':'whole procedure withheld','instance_scope':self.current_hierarchy})
                    self.procedure_notes.append({**self.source(p),'instance_scope':self.current_hierarchy,'original_kind':p['procedureKind'],'scope':'statement-position blocking SSA'})
                else:
                    self.body['members']=[p]
                    # Call RichAdapter (not NaturalAdapter) for clocked/continuous.
                    from spi_semantic_v2 import RichAdapter
                    RichAdapter.extract(self)
        finally:self.body['members']=members;self.environment=None;self.blocking_writes=set()
        return self


class HierarchyBitVectors(NaturalBitVectors):
    def _collect_definitions(self):
        # Aggregate disjoint, completely assigned packed slices. Partial or
        # overlapping drivers are unresolved, never zero-filled as an assumption.
        grouped=defaultdict(list)
        for p in self.adapter.body['members']:
            if p.get('kind')!='ContinuousAssign':continue
            a=p['assignment']
            try:
                lhs=self.adapter.typed(a['left']);rhs=self.adapter.typed(a['right']);offset=0;base=lhs
                if lhs['kind'] in ('Slice','MemberAccess'):
                    offset=lhs.get('offset',lhs.get('bit_offset'));base=lhs['value']
                if base['kind']!='NamedValue':raise Unsupported('Indirect continuous lvalue')
                if lhs['type']['width']!=rhs['type']['width']:raise Unsupported('Unelaborated connection sizing')
                grouped[self.name(base)].append((base,offset,lhs['type']['width'],rhs,p))
            except Unsupported as e:self.unresolved.append({'source':self.adapter.source(p),'reason':str(e)})
        for key,parts in grouped.items():
            base=parts[0][0];w=base['type']['width'];used=set();valid=True
            for _,o,pw,_,p in parts:
                bits=set(range(o,o+pw))
                if o<0 or o+pw>w or used&bits:valid=False
                used|=bits
            if not valid or used!=set(range(w)):
                self.unresolved.append({'signal':base['symbol'],'reason':'Overlapping or incomplete continuous packed driver'});continue
            if len(parts)==1 and parts[0][1]==0:rhs=parts[0][3]
            else:
                rhs={'kind':'Concatenation','type':base['type'],'operands':[r for _,_,_,r,_ in sorted(parts,key=lambda x:x[1],reverse=True)]}
            self.definitions[key]=rhs;self.definition_sources[key]={'lhs':base,'rhs':rhs,'source':self.adapter.source(parts[0][4]),'method':'disjoint complete packed continuous assignment / directed port connection','port_alias':any(p.get('_port_alias') for *_,p in parts)}

    def term(self,node):
        if node['kind']=='MemoryRead':
            key=self.name(node);self.variables[key]=node;return key
        if node['kind']=='TotalSelect':
            w=node['type']['width'];sw=node['selector']['type']['width'];s=self.term(node['selector']);v=self.term(node['value'])
            if node['elements']!=1<<sw or node['value']['type']['width']!=node['elements']*w:raise Unsupported('Total select domain mismatch')
            out=f'((_ extract {w-1} 0) {v})'
            for i in range(1,node['elements']):out=f'(ite (= {s} {self.literal(i,sw)}) ((_ extract {(i+1)*w-1} {i*w}) {v}) {out})'
            return out
        return super().term(node)
