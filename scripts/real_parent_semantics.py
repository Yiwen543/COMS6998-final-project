"""Add packed lvalue handling for original parent integrations.

Previous scope adapters stay hash-stable. All new assignments require an
independent Yosys-cell proof before use in semantic feedback.
"""
import copy
import hierarchy_semantics as previous
from hierarchy_semantics import HierarchyAdapter,HierarchyBitVectors
from slang_guard_adapter import Unsupported

class ParentAdapter(HierarchyAdapter):
    def typed(self,node):
        if node['kind']=='ParentTyped':return node['typed']
        return super().typed(node)

    def extract(self):
        saved=previous.HierarchyBitVectors
        try:
            previous.HierarchyBitVectors=ParentBitVectors
            return super().extract()
        finally:previous.HierarchyBitVectors=saved

class ParentBitVectors(HierarchyBitVectors):
    def _collect_definitions(self):
        original=self.adapter.body['members'];view=[]
        def parts(lhs,rhs,offset=0):
            if lhs['kind']=='Concatenation':
                out=[]
                for n in reversed(lhs['operands']):
                    out+=parts(n,rhs,offset);offset+=self.adapter.type_info(n['type'])['width']
                return out
            width=self.adapter.type_info(lhs['type'])['width']
            if offset<0 or offset+width>rhs['type']['width']:raise Unsupported('Concat connection width mismatch')
            return [(lhs,{'kind':'Slice','type':self.adapter.type_info(lhs['type']),'value':rhs,'offset':offset})]
        for p in original:
            if p.get('kind')=='ContinuousAssign' and p['assignment']['left']['kind']=='Concatenation':
                a=p['assignment']
                try:
                    rhs=self.adapter.typed(a['right'])
                    if self.adapter.type_info(a['left']['type'])['width']!=rhs['type']['width']:raise Unsupported('Concat connection sizing')
                    for lhs,part in parts(a['left'],rhs):view.append({**p,'assignment':{**a,'left':lhs,'right':{'kind':'ParentTyped','typed':part}}})
                except Unsupported:view.append(p)
            else:view.append(p)
        self.adapter.body['members']=view
        try:super()._collect_definitions()
        finally:self.adapter.body['members']=original

    @staticmethod
    def packed_insert(old,part,offset,info):
        width=info['width'];pw=part['type']['width']
        if offset==0 and pw==width:return part
        node={'kind':'Insert','type':info,'value':old,'part':part,'offset':offset}
        covered=set();n=node
        while n.get('kind')=='Insert':
            covered.update(range(n['offset'],n['offset']+n['part']['type']['width']));n=n['value']
        if covered!=set(range(width)):return node
        # Every bit is explicitly assigned. Select its latest write; do not
        # leave an artificial Uninitialized subtree or assume an initial zero.
        def bit(i,n):
            if n['kind']=='Insert':
                if n['offset']<=i<n['offset']+n['part']['type']['width']:
                    return {'kind':'Slice','type':{'width':1,'signed':False,'four_state':info['four_state']},'value':n['part'],'offset':i-n['offset']}
                return bit(i,n['value'])
            raise Unsupported('Incomplete packed assignment')
        return {'kind':'Concatenation','type':info,'operands':[bit(i,node) for i in reversed(range(width))]}

    def _statement(self,node,env):
        if node and node.get('kind')=='ExpressionStatement':
            a=node['expr']
            if a.get('kind')=='Assignment' and not a.get('isNonBlocking') and a['left']['kind'] in ('ElementSelect','RangeSelect'):
                with self.adapter.scope(None):
                    lhs=self.adapter.typed(a['left']);base=lhs.get('value')
                    if lhs['kind']!='Slice' or base['kind']!='NamedValue':raise Unsupported('Only static packed partial writes supported')
                    key=self.name(base);rhs=self._expression(a['right'],env)
                    if rhs['type']['width']!=lhs['type']['width']:raise Unsupported('Partial assignment width mismatch')
                    result=dict(env);result[key]=self.packed_insert(env[key],rhs,lhs['offset'],base['type']);return result
        return super()._statement(node,env)
