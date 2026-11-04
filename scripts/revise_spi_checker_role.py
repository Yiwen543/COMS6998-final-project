#!/usr/bin/env python3
"""Claude-authored exact patches, deterministic controls, fresh independent Claude review."""
import argparse
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path
from run_midterm_fixed import ROOT, sha
from run_claude_divider_audit import KEY_FILE, validate_model
from run_spi_checker_author import validate_source
from evaluate_spi_checker_candidate import evaluate

FILES=('checker.py','selftest.py','properties.json','contract.md')


def call(prompt, output, env, role):
    output.mkdir(parents=True,exist_ok=False)
    (output/'prompt.txt').write_text(prompt)
    command=['claude','--bare','--restricted','--print','--model','claude-opus-5-5',
        '--no-session-persistence','--permission-mode','dontAsk','--tools','',
        '--disable-slash-commands','--strict-mcp-config','--setting-sources','',
        '--effort','low','--max-budget-usd','4','--output-format','stream-json','--verbose',
        '--system-prompt',f'You are the independent {role} role. Use only the supplied packet. No tools.']
    start=time.perf_counter()
    meta={'role':role,'requested_model':'claude-opus-5-5','tools':[], 'budget_usd':4,
          'timeout_seconds':600,'command':command,'prompt_sha256':sha(output/'prompt.txt'),
          'usage_status':'unknown_until_complete; a failed call is not zero-cost'}
    try:
        with tempfile.TemporaryDirectory(prefix='spi-checker-role-') as cwd, \
             (output/'stream.jsonl').open('w') as stdout, (output/'stderr.log').open('w') as stderr:
            p=subprocess.run(command,input=prompt,text=True,stdout=stdout,stderr=stderr,
                             cwd=cwd,env=env,timeout=600)
        if p.returncode: raise RuntimeError('Claude process failed')
        rs=[json.loads(l) for l in (output/'stream.jsonl').read_text().splitlines()]
        result=next(r for r in reversed(rs) if r.get('type')=='result')
        (output/'response.json').write_text(json.dumps(result,indent=2)+'\n')
        validate_model(result,role)
        meta.update(usage=result.get('usage'),model_usage=result.get('modelUsage'),
                    total_cost_usd=result.get('total_cost_usd'),usage_status='reported_by_Claude_Code')
        if result.get('is_error'):raise RuntimeError('Claude returned error')
        text=str(result.get('result','')).strip()
        if text.startswith('```'):text='\n'.join(text.splitlines()[1:-1])
        parsed=json.loads(text)
        meta['status']='complete'
        return parsed
    except Exception as e:
        meta.update(status='failed',error_type=type(e).__name__)
        raise
    finally:
        meta['wall_seconds']=time.perf_counter()-start
        (output/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')


def run(base, output, prior=None):
    output.mkdir(parents=True,exist_ok=False)
    (output/'runner-source.py').write_bytes(Path(__file__).read_bytes())
    prior=prior or base/'claude-author-v2'
    previous=json.loads((prior/'metadata.json').read_text())
    sources={f:(prior/f).read_text() for f in FILES}
    for f in FILES:
        if sha(prior/f)!=previous['artifact_sha256'][f]:raise ValueError('Prior checker edited')
    spec=json.loads((base/'spec-packet/packet.json').read_text())
    controls=json.loads((base/'evaluation-v2/private-validation-inputs.json').read_text())
    feedback={
        'independent_positive_reference':controls['independent_reference/one_byte_write'],
        'observed_result':json.loads((base/'evaluation-v2/evaluations.json').read_text())['cases']['independent_reference/one_byte_write'],
        'review_findings':[
            'The independently authored legal one-byte trace accepts a command and performs its first wr on the SAME rising edge. Your loop processes wr before adding the accepted command, producing a false stale_byte. Resolve simultaneous operations using command/byte FIFO semantics; do not prohibit this input.',
            'A changed CSID can be offered while old CSAAT selection is active; old CS can release BEFORE new ready/acceptance. Your switch object is only created at acceptance and misses earlier release/gap. Track pending offers, bind eventual acceptance, and handle reset/cancellation assumptions without inventing an acceptance requirement for old CS release.',
            'Your csaat_hold check likewise permits release only when accept is true, though the spec allows queued changes before acceptance.',
            'The public spec has old AND new idle requirements for configuration changes. max(old,new) with arbitrary one-cycle tolerance is not a proof of both; enforce justified bounds where observable, otherwise mark this obligation blocking unresolved for that switch.',
            'Event completion must not be inferred from half the required SPI clocks or only last/ready/active. Review your enough() lower bound and lack of missing-byte-at-deselection failures. Ensure a truncated or too-short burst cannot be called complete.',
            'Check last flags without byte transfer and transfer while external readiness is false; currently these may be missed. Distinguish unsupported active/reset outputs from tested properties in the manifest.',
        ],
        'constraints':'This is checker-infrastructure correction on independent controls, not fitting to DUT or B/C outcomes. No DUT implementation or model outcomes are supplied. Do not force any real DUT trace to pass. Keep unresolved timing/reset assumptions explicit; do not weaken checks to obtain event counts.'}
    if (prior.parent/'review.json').exists():
        feedback={'independent_review':json.loads((prior.parent/'review.json').read_text()),
            'scope':'Correct the review-confirmed event-window failure gating and property/code inconsistencies. Keep unsupported active/last-without-transfer outputs explicitly out of scope; do not claim detection or silently drop those controls. Preserve pending/inconclusive cases. Do not fit to the DUT.',
            'specific_controls':'The next independent control set also includes a wrong select on the SECOND held software-reset cycle, a select change during actual stall, rd asserted with sink not ready, a stale wr on the first reset-release cycle before any acceptance, and an idle SCK edge inconsistent with the previous CPOL. Your own tests must include event-window faults, not only nonzero failures.',
            'author_task':'Return small exact patches and new self-tests. Event evidence is valid only if its complete inclusive [start_cycle,end_cycle] window has no checker/assumption violation. Correct reset/stall entry snapshots. Reconcile P10/P15 with the implemented and justified scope. Select-specific timing attribution and any unproven additive timing must be checked or blocking unresolved; do not report unsupported cases as qualified.'}
    prompt='''Revise your previously generated checker as its independent author role. Return ONLY JSON with keys patches and rationale.
patches is a list of {file,before,after}; allowed files checker.py,selftest.py,properties.json,contract.md. Each before must be a unique nonempty EXACT substring of that file. Apply patches in order. Avoid rewriting unchanged code. All corrections must be your own source edits, not delegated to the stimulus author.
Add meaningful independent positive/negative controls for same-edge accept+wr, release-before-accept switching, and incomplete/missing-byte behavior. Preserve existing useful controls. Be concise; no entire-file rewrite unless unavoidable. No filesystem or network code; only collections/copy/math and builtins.
SPEC AND INTERFACE:\n'''+json.dumps(spec,separators=(',',':'))+'\nCURRENT FILES:\n'+json.dumps(sources,separators=(',',':'))+'\nINDEPENDENT REVIEW:\n'+json.dumps(feedback,separators=(',',':'))
    consumed=False
    try:
        if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:raise RuntimeError('Hidden key missing/unsafe')
        env=dict(os.environ);env['ANTHROPIC_API_KEY']=KEY_FILE.read_text().strip();consumed=True
        for k in list(env):
            if k.startswith(('OPENAI_','ANTHROPIC_BASE_URL','CLAUDE_CODE_USE_')):env.pop(k)
        patch=call(prompt,output/'author-call',env,'specification_checker_author_revision')
        (output/'patches.json').write_text(json.dumps(patch,indent=2)+'\n')
        for item in patch['patches']:
            f,before,after=item['file'],item['before'],item['after']
            if f not in FILES or not before or sources[f].count(before)!=1:
                raise ValueError('Patch does not match uniquely; never guess or edit manually')
            sources[f]=sources[f].replace(before,after,1)
        validate_source(sources['checker.py']);validate_source(sources['selftest.py'])
        json.loads(sources['properties.json'])
        candidate=output/'candidate';candidate.mkdir()
        for f,text in sources.items():(candidate/f).write_text(text)
        (candidate/'response.json').write_bytes((output/'author-call/response.json').read_bytes())
        manifest={'status':'candidate_generated_not_validated','role':'claude-opus-5-5 checker author',
            'parent_checker_sha256':previous['artifact_sha256']['checker.py'],
            'patch_response_sha256':sha(output/'patches.json'),
            'artifact_sha256':{f:sha(candidate/f) for f in FILES},
            'integration_policy':'Only exact Claude-authored patches applied; GPT made no checker source edits.'}
        (candidate/'metadata.json').write_text(json.dumps(manifest,indent=2)+'\n')
        evaluation=evaluate(candidate,base/'calibration',output/'evaluation')
        # Fresh tool-free session audits source + spec + public findings, not prior
        # model reasoning or hidden performance-arm labels.
        review_packet={'spec_and_interface':spec,'checker_source':sources['checker.py'],
            'properties':json.loads(sources['properties.json']),'evaluation':evaluation,
            'independent_reference':controls['independent_reference/one_byte_write'],
            'switch_observations':{n:[r for r in controls['calibration/'+n] if r['action']['valid'] or r['pre']['csb']!=r['post']['csb']]
                                   for n in ('csid_switch','configuration_switch')}}
        review_prompt='''Independently review the checker and evidence in this packet. Do not edit code, invent coverage, generate stimulus, or presume DUT traces must pass. Identify remaining checker errors, unsupported assumptions, false-positive controls, missed negative controls, and whether the configuration-switch behavior is a possible specification violation versus an instrumentation error. No RTL implementation is provided; say which conclusions need it. Judge whether each selected event family can be qualified. This is not an A/B/C outcome review. Return ONLY JSON: {findings:[{status,category,evidence,impact}], ready_to_freeze:boolean, required_followup:[strings]}.\n'''+json.dumps(review_packet,separators=(',',':'))
        review=call(review_prompt,output/'independent-review',env,'independent_checker_and_evidence_reviewer')
        (output/'review.json').write_text(json.dumps(review,indent=2)+'\n')
        return {'candidate':str(candidate),'review_ready_to_freeze':review['ready_to_freeze']}
    finally:
        if consumed:KEY_FILE.unlink(missing_ok=True)


def prepare_review(base, revision, output):
    output.mkdir(parents=True,exist_ok=False)
    candidate=revision/'candidate'
    manifest=json.loads((candidate/'metadata.json').read_text())
    for f,digest in manifest['artifact_sha256'].items():
        if sha(candidate/f)!=digest:raise ValueError('Candidate changed before review')
    controls=json.loads((revision/'evaluation/private-validation-inputs.json').read_text())
    packet={'spec_and_interface':json.loads((base/'spec-packet/packet.json').read_text()),
        'checker_source':(candidate/'checker.py').read_text(),
        'properties':json.loads((candidate/'properties.json').read_text()),
        'evaluation':json.loads((revision/'evaluation/summary.json').read_text()),
        'control_accounting':json.loads((revision/'evaluation/control-accounting.json').read_text()),
        'independent_reference':controls['independent_reference/one_byte_write'],
        'prior_findings':json.loads((base/'revision-v3/review.json').read_text()),
        'configuration_discrepancy_reproducer':json.loads((base/'config-switch-reproducer/evidence.json').read_text()),
        'full_public_switch_trace':controls['calibration/configuration_switch'],
        'fixed_driver_source':(ROOT/'examples/heldout_spi_host/verif/tb_spi_host_fixed.sv').read_text(),
        'rtl_scope':'Only the separate reviewer sees the quoted DUT excerpts. The checker author was not given RTL.'}
    prompt='''Independently review the corrected checker and the empirical evidence; no code changes, no stimulus generation. This fresh reviewer session is distinct from the checker-author session. Check whether the previous event-window false positives were fixed, property text matches executable scope, positive controls pass and negatives are credited only against clean baselines. Two old controls are explicitly outside the declared checker scope; retain them as not detected, do not count them as successes or demand hidden widening of scope. Determine whether the remaining scoped checker is adequate for offline event qualification; distinguish this from formal A/B/C readiness, which also requires source-target bindings absent here. Configuration-switch reproduction now includes full public trace, fixed driver and relevant pinned RTL excerpts. Assess evidence for a scoped spec/implementation discrepancy and remaining full-IP/formal limits. Do not presume the DUT must pass. Return ONLY JSON: {findings:[{status,category,evidence,impact}], ready_to_freeze:boolean, required_followup:[strings]}.\n'''+json.dumps(packet,separators=(',',':'))
    (output/'packet.json').write_text(json.dumps(packet,indent=2)+'\n')
    (output/'prompt.txt').write_text(prompt)
    return prompt


def review_only(prepared, output):
    # Packet is prepared and checked before touching the credential.
    prompt=(prepared/'prompt.txt').read_text()
    if not KEY_FILE.exists() or KEY_FILE.stat().st_mode & 0o077:raise RuntimeError('Hidden key missing/unsafe')
    env=dict(os.environ);env['ANTHROPIC_API_KEY']=KEY_FILE.read_text().strip()
    for k in list(env):
        if k.startswith(('OPENAI_','ANTHROPIC_BASE_URL','CLAUDE_CODE_USE_')):env.pop(k)
    try:
        result=call(prompt,output,env,'independent_checker_and_evidence_reviewer')
        (output/'review.json').write_text(json.dumps(result,indent=2)+'\n')
        return {'review_ready_to_freeze':result['ready_to_freeze']}
    finally:
        KEY_FILE.unlink(missing_ok=True)


if __name__=='__main__':
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--base',type=Path,required=True);cli.add_argument('--output',type=Path,required=True)
    cli.add_argument('--prior',type=Path)
    cli.add_argument('--prepare-review',type=Path,help='Existing revision directory; offline packet only')
    cli.add_argument('--review-only',type=Path,help='Prepared packet; perform the remaining review only')
    args=cli.parse_args()
    if args.prepare_review:
        prompt=prepare_review(args.base.resolve(),args.prepare_review.resolve(),args.output.resolve())
        result={'status':'prepared_without_model_call','prompt_characters':len(prompt)}
    elif args.review_only:
        result=review_only(args.review_only.resolve(),args.output.resolve())
    else:
        result=run(args.base.resolve(),args.output.resolve(),args.prior.resolve() if args.prior else None)
    print(json.dumps(result,indent=2))
