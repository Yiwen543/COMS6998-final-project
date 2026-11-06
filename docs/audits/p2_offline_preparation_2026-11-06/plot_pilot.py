"""Render one figure from saved numeric evidence;no research rerun."""
from pathlib import Path
import json,statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'output/p2/2026-11-06'
data=json.loads((OUT/'pilot-data.json').read_text())
arms=['B2_raw','C2_semantic'];colors=['#285BB1','#008C90']
tokens=[[r['actual_tokens']/1000 for r in data['rows'] if r['arm']==arm] for arm in arms]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none',
                     'axes.spines.top':False,'axes.spines.right':False})
fig,(left,right)=plt.subplots(1,2,figsize=(11.8,5.6),gridspec_kw={'wspace':.36})
fig.subplots_adjust(top=.76,bottom=.24,left=.08,right=.97)
fig.suptitle('Fixed-stimulus monitor pilot: detection ties; C costs more',
             x=.08,y=.97,ha='left',fontsize=18,fontweight='bold')
fig.text(.08,.88,'Saved trace_done controller cohort: 3 independent sessions per arm, 6 rounds per session',
         fontsize=11,color='#526277')
labels=['B: raw feedback','C: + E-graph']
left.bar([0,1],[11,11],color=colors,width=.56,zorder=3)
left.set_xticks([0,1],labels);left.set_ylim(0,12.8);left.set_yticks([0,3,6,9,12])
left.set_ylabel('Distinct observable injected fault types')
left.set_title('Final selected monitors',loc='left',fontweight='bold',pad=16)
for x in [0,1]:left.text(x,11.3,'11 / 11',ha='center',fontsize=14,fontweight='bold')
left.grid(axis='y',alpha=.18,zorder=0)
means=[statistics.mean(v) for v in tokens]
right.bar([0,1],means,color=colors,width=.56,zorder=3,alpha=.9)
for x,values in enumerate(tokens):
    right.scatter([x-.07,x,x+.07],values,s=28,color='#182B45',zorder=5)
    right.text(x,means[x]+10,f'{means[x]:.1f}k',ha='center',fontweight='bold',fontsize=13)
right.set_xticks([0,1],labels);right.set_ylim(0,330);right.set_yticks([0,100,200,300])
right.set_ylabel('Mean actual API tokens per session (thousands)')
right.set_title('Cost across every generation round',loc='left',fontweight='bold',pad=16)
right.grid(axis='y',alpha=.18,zorder=0)
right.text(1,310,f'C: +{data["C_extra_tokens_percent"]:.2f}%',ha='center',color=colors[1],fontweight='bold')
fig.text(.08,.135,'12 raw fault types retained: N10 was unobserved. Unknown contexts remain separate; bars are a finite case/type union.',fontsize=9.5)
fig.text(.08,.090,'Token totals: B 740,643; C 813,649. Dots show the 3 session costs. Cached/reasoning subsets are not added twice.',fontsize=9.5)
fig.text(.08,.045,'Same DUT, reference, fixed inputs, model and caps. No token-matched placebo or statistical/general-correctness claim.',fontsize=9.5)
for suffix in ['png','svg']:
    fig.savefig(OUT/('pilot-bc.'+suffix),dpi=190,facecolor='white')
print('Rendered saved-data figure PNG/SVG;0model/simulator/formal calls.')
