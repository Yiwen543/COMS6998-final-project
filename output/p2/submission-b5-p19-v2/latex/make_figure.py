"""Render the P19 saved-evidence comparison; never invoke an experiment."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'figure-data.json').read_text())
rows=data['rows']
assert [r['actual_tokens'] for r in rows]==[123663,133915]
assert all(r['ordinary_safety_types']==9 and r['finite_case_UNATTRIBUTED_types']==2 and r['raw_type_denominator']==12 for r in rows)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'svg.fonttype':'none','pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
fig,(left,right)=plt.subplots(1,2,figsize=(7.1,2.25),gridspec_kw={'width_ratios':[1,1.15],'wspace':.42})
fig.subplots_adjust(left=.07,right=.985,bottom=.27,top=.84)
navy,teal,gray,orange='#285BB1','#008C90','#E1E5EA','#C57624'
left.bar([0,1],[9,9],width=.48,color=navy,zorder=3)
left.bar([0,1],[2,2],bottom=[9,9],width=.48,color=teal,zorder=3)
left.bar([0,1],[1,1],bottom=[11,11],width=.48,color=gray,edgecolor='#8C96A3',hatch='///',linewidth=.5,zorder=3)
for x in [0,1]:
    left.text(x,4.4,'9',ha='center',va='center',color='white',fontsize=9,fontweight='bold')
    left.text(x,10,'2',ha='center',va='center',color='white',fontsize=8,fontweight='bold')
    left.text(x,12.5,'11/12',ha='center',fontsize=9,fontweight='bold')
left.set_ylim(0,14);left.set_yticks([0,4,8,12]);left.set_ylabel('Raw fault types')
left.set_title('(a) Same detection outcome',loc='left',fontsize=9)
tokens=[row['actual_tokens']/1000 for row in rows]
right.bar([0,1],tokens,width=.48,color=[navy,orange],zorder=3)
for x,row in enumerate(rows):right.text(x,tokens[x]+4,f"{row['actual_tokens']:,}",ha='center',fontsize=9,fontweight='bold')
right.text(.5,154,f"C: +{data['C_extra_tokens_percent']:.2f}% tokens",ha='center',fontsize=8,color=orange,fontweight='bold')
right.set_ylim(0,165);right.set_yticks([0,50,100,150]);right.set_ylabel('Input + output tokens (k)')
right.set_title('(b) All-round generation tokens',loc='left',fontsize=9)
for ax in [left,right]:
    ax.set_xticks([0,1],['B: raw','C: +E-graph']);ax.grid(axis='y',alpha=.16,zorder=0)
fig.legend(handles=[Patch(color=navy,label='Ordinary safety credit'),Patch(color=teal,label='Finite case credit (unattributed)'),Patch(facecolor=gray,edgecolor='#8C96A3',hatch='///',label='N10: no eligible failure')],loc='lower center',bbox_to_anchor=(.50,.005),ncol=3,frameon=False,fontsize=7.5,handlelength=1.2,columnspacing=1.2)
for extension in ['pdf','png','svg']:
    fig.savefig(HERE/'images'/('retest-bc.'+extension),dpi=320,facecolor='white')
plt.close(fig)
print('P19 comparison rendered from saved ledger/grade derivation; no fresh research run.')
