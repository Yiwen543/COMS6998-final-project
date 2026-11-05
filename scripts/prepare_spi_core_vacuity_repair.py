"""Claude-only patch packet for confirmed event-vacuity bugs."""
import argparse
import json
from pathlib import Path
from run_midterm_fixed import ROOT,sha

BASE=ROOT/'results/real_parent_screen_20261104'

def prepare(out):
    prior=BASE/'claude-checker-v3/candidate';p=json.loads((BASE/'contract-repair-v3/packet/packet.json').read_text())
    hashes=json.loads((prior/'authorship.json').read_text())['artifact_sha256']
    if any(sha(prior/f)!=h for f,h in hashes.items()):raise ValueError('Prior Claude artifact drift')
    p['prior_claude_artifacts']={f:(prior/f).read_text() for f in hashes};p['prior_artifact_sha256']=hashes
    p['repair_tasks']=[
        'Preserve the validated word/bit ordering, CPOL idle setup, pending CSID, serial payload/phase/timing and reset separation. Change only event qualification needed below; do not weaken meaningful checks or alter expected payload to fit a DUT.',
        'Confirmed TX event vacuity: temporary absence of the next byte between legal serial edges does not necessarily stall the operation, especially CLKDIV>0. Opening a missing-data candidate and later consuming a new word is insufficient. A completed starvation event must demonstrate an actual delayed/missed serial edge or paused selected operation attributable to absent TX data, then refill and correct completion. A late word that still permits every selected SCK edge at its configured half period must not be called starvation/recovery.',
        'Confirmed RX event vacuity: rx_valid with !rx_ready for a brief interval may be absorbed by buffering with no in-flight operation pause. Require actual backpressure consequence, then drain and correct complete payload. A one-cycle drain delay with uninterrupted normal selected SCK is not a recovery episode.',
        'Stall flags may provide evidence but are not sufficient alone. A forged/contradictory flag with uninterrupted normal selected SCK must never create a successful recovery. Do not create causal temporal equivalences from coverage counters or Boolean guards.',
        'Distinguish candidate wait, confirmed paused episode, resolved episode and successful completion. All confirmed episodes must retain pending/failed/blocked status on truncation/error. A completed no-stall transfer must not retain a spurious pending recovery candidate. Preserve transaction-wide dirty-window rejection and software-reset unresolved status.',
        'Add selftests for late nonstalling refill at a slower divider, brief RX hold without actual pause, flag-only fake recovery, true stall/resume, incomplete genuine stall and bad resumed payload. Use public timing/transport semantics only. No private stimuli, raw DUT trace or implementation is supplied.',
        'The fixed Python stimulus validator already rejects out-of-width values and illegal field combinations before writing vectors. Do not silently mask oversized integers as a checker fix. Keep input assumption failures separate from DUT failures.',
        'Public theory241-249 requires all-CS-high separation before configuration changes after CSAAT. Preserve this requirement and existing explicit unsupported/software-reset limits; do not reinterpret the public contract to make every observed implementation pass.'
    ]
    prompt='You are Claude, the independent SPI core specification checker author. Return ONLY JSON {patches:[{file,before,after}],rationale:...}. Allowed files: checker.py,selftest.py,properties.json,contract.md. Every before must be a nonempty UNIQUE exact substring, patches applied in order. No markdown fences, no whole-file replacement, no tools or stimulus generation. You alone author expected-output changes. Keep pure Python check_rows API and collections/copy/math-only imports. Read the public specification and existing Claude source; retain original contracts and failure history.\n'+json.dumps(p,separators=(',',':'))
    if len(prompt.encode())>150000:raise ValueError('Author cap')
    out.mkdir(parents=True,exist_ok=False);(out/'packet.json').write_text(json.dumps(p,indent=2)+'\n');(out/'prompt.txt').write_text(prompt)
    (out/'manifest.json').write_text(json.dumps({'status':'prepared_not_called','packet_sha256':sha(out/'packet.json'),'prompt_sha256':sha(out/'prompt.txt'),
        'builder_sha256':sha(Path(__file__)),'bytes':len(prompt.encode()),'model':'claude-opus-5-5','calls_planned_max':2,'cli_budget_per_call_usd':4,
        'excludes':['DUT implementation','private stimuli/traces','guards','coverage','B/C outputs']},indent=2)+'\n')
    print(json.dumps({'bytes':len(prompt.encode()),'prior_checker_sha256':sha(prior/'checker.py'),'B_allowed':False}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);prepare(p.parse_args().output.resolve())
