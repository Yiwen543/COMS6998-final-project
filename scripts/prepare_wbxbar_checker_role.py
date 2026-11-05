"""Spec-only author packet for the separately registered exploratory scope."""
import argparse
import json
from pathlib import Path

from run_midterm_fixed import ROOT, sha
from prepare_spi_checker_role import excerpt
from prove_wbxbar_index import configuration
from wbxbar_conditional_semantics import verify_certificate

SCOPE = ROOT / 'configs/wbxbar_exploratory_bc_v1.json'
SPEC = ROOT / 'third_party/wishbone_b4/wbspec_b4.pdf'
SPEC_SHA = 'd712d61fe7f363b671e6b821b7b0259f43ec0b4ce8f3b2072172b2878f347a5a'
PORTS = {
    'inputs': {'i_reset': 1, 'i_mcyc': 2, 'i_mstb': 2, 'i_mwe': 2,
               'i_maddr': 16, 'i_mdata': 64, 'i_msel': 8,
               'i_sstall': 2, 'i_sack': 2, 'i_sdata': 64, 'i_serr': 2},
    'outputs': {'o_mstall': 2, 'o_mack': 2, 'o_mdata': 64, 'o_merr': 2,
                'o_scyc': 2, 'o_sstb': 2, 'o_swe': 2, 'o_saddr': 16,
                'o_sdata': 64, 'o_ssel': 8}}

INSTRUCTIONS = '''You are Claude, the independent specification-checker author. A separate GPT role implements the driver and stimulus.
Return ONLY JSON with exactly checker_source, selftest_source, properties, contract_markdown.
checker_source defines pure Python check_rows(rows), returning failures[{cycle,category,detail}], assumption_violations,
events[{family,kind,start_cycle,end_cycle,evidence}], unresolved, verdict, counts. Verdict is scoped_pass,
dut_violation, input_or_scope_invalid, or unresolved. Return pending obligations separately in counts/unresolved.
Allowed imports: collections, copy, math only. No tools, I/O, filesystem, network, exec/eval, project imports or dunder access.
Derive expected behavior only from cited public specifications and the declared public-pin configuration.
Validate external assumptions separately from DUT violations. Use only pre-edge values for transfers at that edge;
post-edge values describe settled outputs, not a second transaction. Reset is synchronous, not asynchronous.
Establish crossbar request routing, payload preservation, response ownership/order and returned read data from public
transactions, not merely absence of handshake errors. Compare slave-returned data to corresponding master-returned data;
do not assume a memory function or a constant/formula for environmental read data. Do not infer correctness from acceptance alone.
Same-cycle acceptance/response, registered latency and overlapping queued requests must not create false orphan errors.
If identical transactions make ownership observationally ambiguous, preserve uncertainty instead of guessing a master.
Handle pipelined ACK independently of current STB; do not apply the standard-mode STB-to-ACK rule to pipelined traffic.
Do not invent exact arbitration/timeout latency when public prose is insufficient. Mark unproved obligations explicitly.
Decode errors, slave errors, timeout/abort and reset can invalidate outstanding work; do not count aborted work as completed.
An incomplete batch is pending/inconclusive, not a liveness violation or successful recovery. Check complete cumulative traces.
Any claimed event completion requires a witnessed causal sequence and a clean entire window. Events are descriptive only.
Do not edit DUT/driver, produce experimental stimulus, pick targets, count source coverage, or weaken checks to fit observed RTL.
properties is a list of {id,requirement,source,assumptions,support_status}; contract_markdown states exact scope and limitations.
selftest_source defines run(check_rows) returning [{name,pass}], with small independently constructed positive/single-fault traces.
The integration role will add further independent controls; your selftests alone are not certification.
Public source summaries are supplied below. Identify gaps or conflicts as unresolved rather than inventing behavior.'''


def verify_scope():
    prior, candidate = configuration()
    verify_certificate()
    scope = json.loads(SCOPE.read_text())
    if scope['candidate'] != candidate:
        raise ValueError('Original configuration drift')
    for key in ('development_budget', 'model_limits', 'roles'):
        if scope[key] != prior[key]: raise ValueError('Constraint drift: ' + key)
    for entry in ('parent',):
        item = scope[entry]
        if sha(ROOT / item['path']) != item['sha256']:
            raise ValueError('Parent provenance drift')
    for path, digest in scope['evidence_hashes'].items():
        if sha(ROOT / path) != digest: raise ValueError('Evidence drift: ' + path)
    if sha(SPEC) != SPEC_SHA: raise ValueError('Public specification drift')
    if not scope['checker_commission_allowed'] or scope['live_B_allowed'] or scope['live_C_allowed']:
        raise ValueError('This preparation admits checker construction only')
    return scope, candidate


def packet():
    _, c = verify_scope()
    root = ROOT / c['root']
    # Only public introductory comments, never declarations/assignments or internal properties.
    header = excerpt(root / 'rtl/wbxbar.v', [(7,39)])
    for section in header['excerpts']:
        if any(line.strip() and not line.lstrip().startswith('//')
               for line in (root / 'rtl/wbxbar.v').read_text().splitlines()[section['start_line']-1:section['end_line']]):
            raise ValueError('Non-comment text in public introductory excerpt')
    authority = [
        {'source': 'https://cdn.opencores.org/downloads/wbspec_b4.pdf', 'sha256': SPEC_SHA,
         'representation': 'Maintainer paraphrase checked against PDF pages 31–38; not a new protocol specification.',
         'requirements': [
             {'location': '3.1.1, rules 3.00–3.20, pp31–32',
              'summary': 'Reset takes effect on rising clock edges. Hold reset for at least one complete cycle. Master CYC and STB are inactive during reset; other master payload values are unspecified.'},
             {'location': '3.1.2, rules 3.25/3.30, p33',
              'summary': 'CYC qualifies bus activity and spans a transfer cycle. Without CYC, slave request signals are inactive. System reset remains effective.'},
             {'location': '3.1.3.2, rules 3.57–3.59, pp36–37; observation 3.10, p32',
              'summary': 'Pipelined acceptance requires CYC and STB high and STALL low. WE distinguishes writes from reads. New requests need not wait for earlier acknowledgments. ACK can occur while STB is low. Successful transactions retire with acknowledgments; read data is meaningful with ACK.'},
             {'location': 'permission 3.20 / rule 3.45, p35; rule 3.60, p37',
              'summary': 'ERR reports failure; the base protocol leaves the master reaction unspecified. ACK, ERR and RTY cannot coincide. Payload belongs to a strobed request. This interface has no RTY signal.'}]},
        excerpt(root / 'README.md', [(188,196)]), header,
        {'source': 'https://zipcpu.com/blog/2019/07/17/crossbar.html',
         'representation': 'Prose-only intent paraphrase; no implementation examples, expressions or internal signal names included. Older design article is supplementary, not exact-cycle authority.',
         'requirements': [
             {'location': 'What is a Crossbar?; Returning data, paragraphs on nonexistent addresses and abort',
              'summary': 'A crossbar connects masters to slaves without mixing their responses. A request outside every configured address range should return an error. A master may end its cycle to abort outstanding work; completed data must not later be attributed to a new transaction. The article motivates aborting a cycle after an error. Exact buffering, arbitration and timeout edge counts require explicit documentation rather than assumptions.'}]}]
    return {'role': 'Independent specification-only checker author',
            'scope': 'Original WBXBAR public bus boundary, revision ' + c['revision'] + '. Two masters, two slaves. No internal state or submodule observation.',
            'authority': authority, 'parameters': c['parameters'],
            'interface': {'ports': PORTS,
                'packing': 'Port 0 occupies the least-significant slice. Each address is an 8-bit bus address, each data value 32 bits, each select 4 bits. No implicit byte-address shifting.',
                'address_configuration': 'Slave0: (addr & 0xf0)==0x00; slave1: (addr & 0xf0)==0x10. Other addresses match neither slave. This is public parameter decoding, not stimulus guidance.',
                'directions': 'i_m* are external master inputs; o_m* are DUT responses. o_s* are DUT requests to external slaves; i_s* are external slave responses. i_clk is the common clock.',
                'rows': '[{cycle:int, pre:{all listed inputs and outputs}, post:{all listed outputs}}]; integers of declared width. None may represent undefined inactive payload, never a valid active control/data value.',
                'sampling': 'Inputs change while clock low. Pre sampled at +4ns, rising edge at +5ns, post at +9ns, falling edge at +10ns. One row is one physical cycle. Initial trace has two reset cycles followed by quiescence. No extra hidden clock edges.',
                'boundary': 'Checker consumes actual public-pin observations, not model offers or driver queue ledgers. Drivers may queue offers and hold pins through acceptance. Do not trust driver internal accounting as functional truth.',
                'environment_contract': 'External masters obey pipelined acceptance, holding pending request payload through backpressure except explicit cycle abort/reset. External slaves respond in acceptance order, may wait, and do not generate unsolicited responses. Slave work is canceled on cycle withdrawal/reset. Record violations separately from DUT faults. Exact future JSON offer fields are irrelevant to the pin-based checker.'},
            'requested_obligations': ['mapped request routing and payload/byte-mask preservation',
                'response order, destination and read-data preservation across concurrent masters',
                'no invented/duplicated successful transaction, reset and abort epoch separation',
                'unmapped/slave-error response and subsequent restart; timeout scope explicitly justified',
                'pending/unresolved accounting at batch end'],
            'isolation': 'No executable DUT RTL, prior checker, calibrated traces, source targets, coverage results, semantic equivalences or model outcomes.'}


def prepare(output):
    data = packet()
    prompt = INSTRUCTIONS + '\n' + json.dumps(data, separators=(',', ':'))
    if len(prompt.encode()) > 150000: raise ValueError('Author packet byte cap')
    output.mkdir(parents=True, exist_ok=False)
    (output / 'packet.json').write_text(json.dumps(data, indent=2) + '\n')
    (output / 'prompt.txt').write_text(prompt)
    manifest = {'status': 'prepared_not_called', 'scope_sha256': sha(SCOPE),
                'packet_sha256': sha(output / 'packet.json'), 'prompt_sha256': sha(output / 'prompt.txt'),
                'builder_sha256': sha(Path(__file__)), 'bytes': len(prompt.encode()),
                'model': 'claude-opus-5-5', 'calls_planned_max': 2, 'cli_budget_per_call_usd': 4,
                'excluded': ['executable RTL', 'previous checker', 'private calibration', 'coverage/equivalence targets', 'model outcomes'],
                'spec_pdf': {'path': str(SPEC.relative_to(ROOT)), 'url': data['authority'][0]['source'], 'sha256': SPEC_SHA}}
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def verify_packet(folder):
    verify_scope()
    m = json.loads((folder / 'manifest.json').read_text())
    for key, path in [('scope', SCOPE), ('packet', folder / 'packet.json'),
                      ('prompt', folder / 'prompt.txt'), ('builder', Path(__file__))]:
        if m[key + '_sha256'] != sha(path): raise ValueError('Prepared packet drift: ' + key)
    if json.loads((folder / 'packet.json').read_text()) != packet():
        raise ValueError('Packet differs from allowlisted public sources')
    expected = INSTRUCTIONS + '\n' + json.dumps(packet(), separators=(',', ':'))
    if (folder / 'prompt.txt').read_text() != expected: raise ValueError('Prompt content drift')
    return m


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    print(json.dumps(prepare(parser.parse_args().output.resolve()), indent=2))
