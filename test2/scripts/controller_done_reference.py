"""Prepare Claude-only scope review/conditional author packets; no network calls."""
import json
from common import ROOT,BASE,dump,sha
from controller_done_data import TASK,REG,SOURCE_TASK


def prepare():
    out=TASK/'reference/scope-v2';out.mkdir(parents=True,exist_ok=False)
    files=[TASK/'public/specification.md',TASK/'public/observer_contract.md',
           SOURCE_TASK/'reference/frozen-v2/checker.py',
           BASE/'scripts/controller_done_runtime.py',BASE/'scripts/controller_done_score.py',BASE/'scripts/controller_done_witness.py']
    context='\n\n'.join('FILE '+str(p.relative_to(ROOT))+'\n'+p.read_text() for p in files)
    scope='''The original DUT contract and checker input interface are unchanged: byte
interface, MIN4/MAX8, accepted frame1..12, independent data/status channels, reset
flush. Correct and faulty observations come from literal physical DUT simulation.
Development min_tail32 and final min_tail128 use the existing check_rows API.
trace_done is evaluator metadata only,0on all pre/post samples except final post1;
there is no additional DUT clock and the checker does not receive the marker.
No GPT code may silently replace this independent oracle. Synthetic obligation
controls are distinct from physical DUT coverage. A short trace_done0 formal
projection proves neither128cycle completion nor end-only activation. A definite
FAIL may coexist with unknown context: retain both; never label that full PASS.
This review receives no B/C candidate sources, hidden faults, hidden traces, scores
or arm preference. Review from specification, not implementation-majority voting.
'''
    review='''Return JSON only with keys verdict (ACCEPT_SCOPE/LIMITED_SCOPE/REJECT),
scope, issues (list with severity/evidence/required_action), oracle_revision_required
(boolean), adapter_changes_required (boolean), limitations. Independently audit the
provided checker reuse scope and final-post adapter/scoring semantics. Derive from
the specification. Check presented-valid safety including unaccepted responses;
end-only response debts and unaccepted input; reset, tails, unknowns, passive marker,
physical prefix boundary and category overlap. Identify unsupported conclusions.
Do not modify the oracle in this review; request a separate Claude author if needed.
Keep response concise (requested <=3000 output tokens; CLI enforces USD4 budget).
'''+scope+'\n'+context
    author='''CONDITIONAL AUTHOR PACKET, NOT AUTHORIZED OR REQUIRED BY DEFAULT.
Only after an independent scope review demonstrates an oracle/specification gap,
and after separate paid authorization, propose a NEW version of the independent
checker. Keep old frozen checker unchanged. If no actual gap exists, report this;
do not add trace_done as a truth label or weaken unknown/tail semantics.
The invocation must also supply the frozen review issues, not B/C preferences.
Return author schema: checker_source,properties,contract_markdown,selftest_source.
A separate new session must review any authored revision before live candidates.
'''+scope+'\n'+context
    for role,text in [('review',review),('author-conditional',author)]:
        d=out/role;d.mkdir();(d/'prompt.txt').write_text(text)
    dump(out/'manifest.json',dict(status='prepared_not_called',model='claude-opus-5-5',review_calls_proposed=1,
         max_usd_per_call=4,timeout_seconds=600,effort='low',tools=[],independent_session=True,
         output_tokens_requested=3000,hard_output_token_cap=None,hard_cost_cap_usd=4,
         author_calls_currently_authorized=0,reference_reuse='Unchanged scope, pending independent new adapter/scope review',
         checker_sha256=sha(SOURCE_TASK/'reference/frozen-v2/checker.py'),registration_sha256=sha(REG),
         packet_sha256={r:sha(out/r/'prompt.txt') for r in ('review','author-conditional')},
         context_sha256={str(p.relative_to(ROOT)):sha(p) for p in files},API_calls=0))
    return out


if __name__=='__main__':print(prepare())
