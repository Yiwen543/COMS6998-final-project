"""Publication layout for the already measured WBXBAR cost curves."""
import argparse
import json
from pathlib import Path


def plot(run):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    data=json.loads((run/'summary.json').read_text());rows=data['rows']
    config=json.loads((run/'freeze.json').read_text())
    for metric,name in [('branch','coverage-cost'),('toggle','toggle-cost')]:
        fig,axes=plt.subplots(2,2,figsize=(12,8))
        for ax,(field,label) in zip(axes.flat,[('api_tokens','API input + output tokens'),
            ('executed_cycles_including_replays','Physical cycles, including replay'),
            ('simulator_executions','Simulator executions'),('active_wall_seconds','Active session time (seconds)')]):
            for arm in config['arms']:
                for rep in range(1,config['development_budget']['repetitions']+1):
                    rr=[r for r in rows if r['arm']==arm and r['repetition']==rep and r['measurement_fresh'] and r[field] is not None]
                    if rr:ax.plot([r[field] for r in rr],[r['coverage'][metric]['percent'] for r in rr],
                        color={'B':'#2066a8','C':'#c24d26'}[arm],linestyle=['-','--',':'][rep-1],
                        marker='o' if arm=='B' else '^',markersize=4,linewidth=1.4,label=f'{arm}, repetition {rep}')
            ax.set_xlabel(label);ax.set_ylabel(f'Original DUT {metric} points hit (%)');ax.grid(alpha=.2)
        handles,labels=axes[0,1].get_legend_handles_labels()
        fig.suptitle(f'WBXBAR exploratory B/C: {metric} coverage — {data["metadata"]["mode"]}',y=.985)
        fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.95),ncol=3,frameon=False)
        fig.text(.5,.015,'Each marker is a complete measured round. Shared compilation and offline preprocessing are reported separately.',ha='center',fontsize=9)
        fig.tight_layout(rect=(0,.045,1,.87))
        for suffix in ['png','pdf']:fig.savefig(run/(name+'.'+suffix),dpi=170,bbox_inches='tight')
        plt.close(fig)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);plot(p.parse_args().run.resolve())
