from pathlib import Path
from lxml import etree as E
import json
P=Path(__file__).parent
ns='http://www.w3.org/2000/svg';T=lambda n:'{'+ns+'}'+n
base={'header':'64 32 1152 108','footer':'64 662 1152 38','research-question':'64 138 1152 166','proposal':'68 317 1100 88','scope':'68 558 1150 40','semantic-branch':'64 395 1152 64','stimulus-track':'64 483 1152 43','monitor-track':'64 537 1152 43','independence-limit':'64 588 1152 50','invariants':'64 405 1152 92','freeze':'64 511 1152 67','isolation-limit':'64 589 1152 65','queue-target-cost':'76 238 780 340','result-summary':'884 245 332 320','coverage-endpoints':'64 579 1152 74','monitor-token-cost':'64 246 720 258','fixed-endpoint':'842 221 374 225','formal-disclosure':'64 512 1152 94','secondary-limit':'64 609 1152 43','interpretation':'64 154 1152 95','planning-limits':'64 568 1152 45','feedback-request':'64 617 1152 32'}
for f in sorted((P/'svg_output').glob('*.svg')):
 n=int(f.name[:2]);root=E.parse(str(f)).getroot()
 for g in root.findall(T('g')):g.set('data-pptx-bounds',base[g.get('id')])
 new={}
 def take(c,key,bounds):
  if key not in new:
   g=E.Element(T('g'),id=key);g.set('data-pptx-bounds',bounds);new[key]=g
  root.remove(c);new[key].append(c)
 for i,c in enumerate(list(root)):
  if not isinstance(c.tag,str) or c.tag==T('g'):continue
  x=float(c.get('x',c.get('x1','0')));y=float(c.get('y',c.get('y1','0')))
  if c.tag==T('rect') and (c.get('width')=='1280' or (n==1 and x==1004)):
   c.set('data-pptx-role','background');c.set('id','page-background' if x==0 else 'cover-side-field');continue
  if n==1:
   if y<110:
    if c.tag==T('rect'):c.set('data-pptx-role','decoration');c.set('id','cover-accent');continue
    take(c,'course-kicker','64 32 1152 40')
   elif y>600:take(c,'team-authors','68 602 1150 38')
   else:
    j=0 if x<400 else 1 if x<800 else 2;bx=[68,440,836][j];take(c,f'objective-{j+1}',f'{bx} 437 300 105')
  elif n==2:
   if y<200:take(c,'prototype-lead','64 145 1152 42')
   else:take(c,'generation-tool-loop','64 220 1152 148')
  elif n==3:
   if y<200:take(c,'method-lead','64 145 1152 42')
   else:
    side='b' if x<656 else 'c';bx=64 if side=='b' else 656;take(c,f'arm-{side}',f'{bx} 211 560 176')
  elif n==4:
   if y<190:take(c,'queue-study-scope','64 145 1152 42')
   elif y<230:take(c,'queue-chart-title','64 195 1152 38')
   elif c.tag==T('line') and x==884:
    root.remove(c);next(g for g in root.findall(T('g')) if g.get('id')=='result-summary').insert(0,c)
   else:
    root.remove(c);next(g for g in root.findall(T('g')) if g.get('id')=='queue-target-cost').append(c)
  elif n==5:take(c,'monitor-study-scope' if y<200 else 'monitor-chart-title','64 145 1152 42' if y<200 else '64 199 1152 36')
  elif n==6:
   j=0 if y<380 else 1 if y<475 else 2;yy=[294,390,486][j];take(c,f'proposed-step-{j+1}',f'64 {yy} 1152 76')
 for g in new.values():root.append(g)
 for m in root.iter(T('metadata')):
  d=json.loads(m.text);d['data_labels']={'show_value':True,'number_format':'0.0','position':'outEnd'}
  if d['name']=='monitor-token-cost':d['categories']=['B','C']
  else:d['show_legend']=True;d['legend_position']='top'
  m.text=json.dumps(d)
 f.write_bytes(E.tostring(root,encoding='utf-8'))
print('Root modules now follow the actual non-overlapping semantic layout.')
