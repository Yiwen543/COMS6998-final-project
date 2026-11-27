"""Render the two-panel Milestone 3 evidence figure from archived Mac data."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'figure_data.json').read_text())
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8.2,
                     'pdf.fonttype': 42, 'axes.titlesize': 9.0,
                     'axes.labelsize': 8.0, 'axes.spines.top': False,
                     'axes.spines.right': False})
BLUE, TEAL, GRAY, DARK = '#2756a6', '#00858a', '#a9b5c2', '#172a40'
fig = plt.figure(figsize=(7.14, 1.82), facecolor='white')
a = fig.add_axes([.018, .10, .445, .81])
a.set_xlim(0, 1); a.set_ylim(0, 1); a.axis('off')
a.set_title('(a) Real scoped-proof lifecycle', pad=4)
a.text(.5, .86, 'Stale proof blocked at both switches', ha='center', color='#454545', fontsize=8)
for i, (x, stage) in enumerate(zip((.15, .5, .85), DATA['live_stages'])):
    scope = stage['guard'].split()[-1].rstrip(')')
    fill = BLUE if stage['status'] == 'Replay' else TEAL
    box = FancyBboxPatch((x-.126, .29), .252, .42, boxstyle='round,pad=0.016,rounding_size=0.018',
                         fc=fill, ec='none', transform=a.transAxes)
    a.add_patch(box)
    a.text(x, .625, f'N = {scope}', ha='center', va='center', color='white', weight='bold', fontsize=9)
    a.text(x, .48, stage['status'], ha='center', va='center', color='white', fontsize=8.1)
    a.text(x, .365, f"{stage['steps']} steps", ha='center', va='center', color='white', fontsize=8.1)
    if i < 2:
        a.annotate('', xy=(x+.205,.50), xytext=(x+.145,.50), arrowprops=dict(arrowstyle='->', color=DARK, lw=1.2))
a.text(.5, .13, 'Equivalent replies in all three feedback arms', ha='center', fontsize=8, color='#333333')

b = fig.add_axes([.653, .235, .318, .675])
counts = DATA['portfolio_09']
keys=['egg_eager','egg_dependency_triage','ordinary_dependency_triage','smt_subscope']
labels=['Eager Egg','Egg reuse + triage','Ordinary + triage','Direct SMT']
values=[counts[k] for k in keys]
colors=[GRAY, BLUE, TEAL, '#777777']
b.barh(range(4), values, height=.63, color=colors, zorder=3)
b.set_yticks(range(4), labels=labels); b.invert_yaxis()
b.tick_params(axis='y', length=0, pad=4, labelsize=7.7)
b.tick_params(axis='x', length=3, labelsize=7.6)
b.set_xlim(0, 2450); b.set_xticks([0,1000,2000]); b.set_xlabel('Typed SMT checks', labelpad=1)
b.xaxis.grid(True, color='#dddddd', linewidth=.6, zorder=0)
b.spines['left'].set_visible(False)
for y, v in enumerate(values):
    b.text(v+42, y, f'{v:,}', va='center', ha='left', fontsize=8, fontweight='bold', color='#202020')
b.set_title('(b) Nine-property control', pad=5, x=.42)
fig.savefig(ROOT/'figure1.pdf', metadata={'Title':'Scoped proof lifecycle and typed query costs'})
fig.savefig(ROOT/'figure1.png', dpi=200)
