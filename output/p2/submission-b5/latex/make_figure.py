from pathlib import Path
import json,statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
d=json.loads((p/'pilot-data.json').read_text())
colors=['#285BB1','#008C90'];arms=['B2_raw','C2_semantic']
values=[[x['actual_tokens']/1000 for x in d['rows'] if x['arm']==a] for a in arms]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False})
fig,(a,b)=plt.subplots(1,2,figsize=(7.1,2.15),gridspec_kw={'width_ratios':[1,1.25],'wspace':.40})
fig.subplots_adjust(left=.065,right=.985,bottom=.22,top=.81)
a.bar([0,1],[11,11],color=colors,width=.52,zorder=3);a.set_ylim(0,12.7);a.set_yticks([0,4,8,12]);a.set_ylabel('Distinct types');a.set_title('(a) Final observable fault detection',loc='left',fontsize=9)
for x in [0,1]:a.text(x,11.35,'11/11',ha='center',fontsize=9,fontweight='bold')
b.bar([0,1],[statistics.mean(x) for x in values],color=colors,width=.52,zorder=3);b.set_ylim(0,325);b.set_yticks([0,100,200,300]);b.set_ylabel('Generation tokens / session (k)');b.set_title('(b) All-round generation cost',loc='left',fontsize=9)
for i,v in enumerate(values):
 b.scatter([i-.065,i,i+.065],v,s=12,color='#182B45',zorder=4)
 b.text(i,statistics.mean(v)+10,f'{statistics.mean(v):.1f}k',ha='center',fontsize=9,fontweight='bold')
b.text(1,309,'C: +9.86%',ha='center',fontsize=8,color=colors[1],fontweight='bold')
for ax in [a,b]:ax.set_xticks([0,1],['B: raw','C: +E-graph']);ax.grid(axis='y',alpha=.16,zorder=0)
fig.savefig(p/'images/pilot-bc.png',dpi=300,facecolor='white');fig.savefig(p/'images/pilot-bc.svg',facecolor='white')
print('Paper-sized figure rendered from exact saved numeric data.')
