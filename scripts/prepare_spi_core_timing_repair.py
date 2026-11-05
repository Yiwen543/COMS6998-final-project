"""Prepare another Claude-authored patch; no private stimulus or DUT source."""
import argparse
import json
from pathlib import Path
from run_midterm_fixed import ROOT,sha

BASE=ROOT/'results/real_parent_screen_20261104'

def prepare(out):
    prior=BASE/'claude-checker-v2/candidate';old=json.loads((BASE/'contract-repair-v2/packet/packet.json').read_text())
    hashes=json.loads((prior/'authorship.json').read_text())['artifact_sha256']
    for f,h in hashes.items():
        if sha(prior/f)!=h:raise ValueError('Author artifact drift')
    old['prior_claude_artifacts']={f:(prior/f).read_text() for f in hashes};old['prior_artifact_sha256']=hashes
    old['repair_tasks']=[
      'Preserve the validated registered LSB-first word contract, pending valid CSID handling and all existing byte/phase/timing checks. Fix only remaining temporal attribution and event completeness.',
      'CPOL: theory35-37 and241 define idle polarity and reconfiguration while all CSB are high. Such an idle-level setup transition is not a selected payload leading/trailing edge and must not pop the queued segment or increment edge parity. Still enforce correct CPOL at CS assertion, and real selected-edge timing/data checks; do not silently allow uncommanded serial activity.',
      'TX starvation still returns no events on complete and truncated controls. Track missing input using enabled-byte availability, not merely the word index: after last enabled byte is consumed bp may already exhaust the word while wi has not advanced. Pauses can begin after the last sampling edge of a byte BEFORE its trailing edge; whole-bit edge-count divisibility misses this case. Trigger must be detected while paused, not retrospectively only at a resume sample. Resolution may accept a word before the postponed trailing edge. Keep non-destructive availability accounting, actual correct transfer completion and clean transaction window separate.',
      'Every independently witnessed in-flight starvation episode must produce pending, failed, blocked or pass event. Incomplete / missing input / no completion cannot yield an empty event list or success. A correct completed transfer with a pause and later refill should produce the intended event; a dirty resumed payload must fail it. Hardware vs software reset semantics remain separate and unresolved obligations stay unresolved.',
      'Add selftests that specifically cover CPOL1 idle setup before CS assertion followed by good/bad payload, exhausted byte-enable cursor, a postponed trailing edge, word acceptance before resume and truncated/dirty starvation. These are logical requirements only; no DUT or private calibration sequence is supplied.',
      'Independent controls now include all CPOL/CPHA modes and widths, nonzero timing, and nonuniform standard RX for FULLCYC0/1. Claim support only as justified by public specification. Do not reclassify legal modes as invalid to suppress false positives.'
    ]
    text='You are Claude, the independent original SPI core checker-author role. Only you may modify expected-output logic. Return ONLY JSON {patches:[{file,before,after}],rationale:...}. Files: checker.py,selftest.py,properties.json,contract.md. Each nonempty before must occur exactly once, patches apply in order. No whole-file replacements or markdown fences. No tools, DUT implementation, private stimulus or coverage/results. Use public specification and the existing Claude source. Keep pure Python API check_rows and collections/copy/math-only imports.\n'+json.dumps(old,separators=(',',':'))
    if len(text.encode())>150000:raise ValueError('Packet cap')
    out.mkdir(parents=True,exist_ok=False);(out/'packet.json').write_text(json.dumps(old,indent=2)+'\n');(out/'prompt.txt').write_text(text)
    (out/'manifest.json').write_text(json.dumps({'status':'prepared_not_called','packet_sha256':sha(out/'packet.json'),'prompt_sha256':sha(out/'prompt.txt'),'builder_sha256':sha(Path(__file__)),
      'bytes':len(text.encode()),'calls_planned_max':2,'cli_budget_per_call_usd':4,'model':'claude-opus-5-5','excluded':['DUT source','private controls','coverage','B/C results']},indent=2)+'\n')
    print(json.dumps({'packet_bytes':len(text.encode()),'prior_checker_sha256':sha(prior/'checker.py'),'B_allowed':False}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);prepare(p.parse_args().output.resolve())
