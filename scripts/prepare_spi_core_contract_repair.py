"""Register a source-backed contract correction, then prepare Claude-only patches.

No checker source is edited here. Historical packets/results remain immutable.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from prepare_spi_checker_role import excerpt
from real_parent_screen import configuration, verify, SCOPE
from run_midterm_fixed import ROOT, sha

BASE = ROOT/'results/real_parent_screen_20261104'
PRIOR = BASE/'claude-checker-v1/candidate'
FILES = ('checker.py', 'selftest.py', 'properties.json', 'contract.md')


def write(path, obj):
    path.write_text(json.dumps(obj, indent=2)+'\n')


def prepare(out):
    c = configuration('spi_host_core'); verify(c)
    root = ROOT/c['root']; pin = c['revision']
    doc = root/'hw/ip/spi_host/doc'
    authority = out/'authority'; authority.mkdir(parents=True, exist_ok=False)
    citations = [
        ('hw/ip/spi_host/doc/theory_of_operation.md', [(395,419),(478,483),(685,702),(729,740)], 'normative with explicit internal contradiction'),
        ('hw/ip/spi_host/doc/programmers_guide.md', [(65,90),(114,121)], 'software-visible intended byte order'),
        ('hw/ip/spi_host/doc/registers.md', [(323,365)], 'register-interface intended byte order'),
        ('hw/ip/spi_host/rtl/spi_host.sv', [(427,460),(484,520)], 'integration boundary only, not a golden functional model'),
        ('hw/ip/spi_host/rtl/spi_host_data_fifos.sv', [(54,99),(104,124)], 'identity/permutation wiring outside selected core'),
    ]
    evidence = []
    for path, ranges, role in citations:
        f = root/path
        expected = subprocess.check_output(['git','-C',str(root),'rev-parse',pin+':'+path], text=True).strip()
        raw = f.read_bytes()
        actual = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if actual != expected: raise ValueError('Upstream blob mismatch: '+path)
        evidence.append({**excerpt(f,ranges), 'upstream_path':path,'git_blob':actual,
                         'url':'https://github.com/lowRISC/opentitan/blob/'+pin+'/'+path,'role':role})
    corroboration=[]
    for local, path in [('dv_README.md','hw/ip/spi_host/dv/README.md'),('spi_host_scoreboard.sv','hw/ip/spi_host/dv/env/spi_host_scoreboard.sv')]:
        f=BASE/'byte-order-authority/upstream'/local; raw=f.read_bytes()
        expected=subprocess.check_output(['git','-C',str(root),'rev-parse',pin+':'+path],text=True).strip()
        actual=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if actual!=expected:raise ValueError('Fetched upstream evidence mismatch: '+path)
        corroboration.append({'path':str(f.relative_to(ROOT)),'sha256':sha(f),'git_blob':actual,
           'url':'https://github.com/lowRISC/opentitan/blob/'+pin+'/'+path,
           'role':'Upstream DV corroboration only; not supplied as checker implementation or treated as formal proof'})
    contract={
        'id':'spi_host_core_public_contract_v2_lsb', 'revision':pin,
        'status':'registered project interpretation supported by pinned upstream intent and boundary wiring; not an upstream maintainer erratum',
        'supersedes_only':'Byte ordering clauses in original spec packet; original MSB-first results remain historical contract-disagreement evidence.',
        'scope':'Unchanged original spi_host_core NumCS=2. No ByteOrder parameter on this core. ByteOrder=1 is used only to relate its pins to documented parent register semantics.',
        'requirements':{
            'tx':'Within each accepted 32-bit word, visit enabled byte lanes in increasing lane index 0,1,2,3. Lane i is bits 8*i+7:8*i and enabled by tx_be[i]. Within each byte transmit most-significant bit/group first. Existing segment discard rules are unchanged.',
            'rx':'Pack successive received bytes b0,b1,b2,b3 into bits 7:0,15:8,23:16,31:24. Short final words have zero padding in unused HIGH lanes. FIFO word order is preserved.',
            'examples':{'tx_0xa1b2c3d4_be15':[212,195,178,161],'tx_0xa1b2c3d4_be5':[212,178],'rx_bytes_a5_5a_3c':'0x003C5AA5'},
            'bit_order':'Byte order is not bit order: each SPI byte remains MSB-first; Standard RX is SD[1], Standard TX SD[0].'},
        'derivation':[
            'Pinned public theory lines 412-419,483, programmer guide and registers independently require LSB-first words / high padding for ByteOrder=1.',
            'Pinned parent instantiates external data FIFOs with SwapBytes=~ByteOrder and explicitly documents natural low-byte-first core behavior. At ByteOrder=1 the FIFOs preserve byte lanes and order in both directions; these are boundary aliases, not an expected-output model.',
            'Therefore the documented LE register semantics transport unchanged to the core word pins. Parent ByteOrder=0 reverses data/BE outside the core and does not change the core contract.',
            'The older component paragraphs 698-702 and735-740 contradict this combination. Mark those ordering statements superseded locally; retain their text and original failed checker. No DUT payload trace is used as normative authority.'
        ],
        'limits':['No claim that upstream maintainers accepted an erratum. Commit history is shallow; no causal history claim.',
                  'No full top-level TLUL verification, four-state proof, formal checker proof or B/C effectiveness claim.',
                  'Software reset and timing gaps remain separate obligations; this correction does not waive them.'],
        'evidence':evidence,'upstream_dv_corroboration':corroboration,
        'unchanged':{'registration_sha256':sha(SCOPE),'driver_sha256':sha(ROOT/'examples/spi_core_integration/verif/tb_spi_core.sv'),
                     'interface_sha256':sha(ROOT/'scripts/spi_core_interface.py'),'DUT_hashes':c['source_hashes'],
                     'budgets_and_gates':json.loads(SCOPE.read_text())['development_budget']},
        'B_allowed':False,'checker_frozen':False}
    write(authority/'contract.json',contract)
    old=json.loads((BASE/'spi-core-spec-packet-v2/packet.json').read_text())
    old['interface']['byte_order']=contract['requirements']
    old['authority'].extend([e for e in evidence if '/doc/' in e['upstream_path']])
    # Author sees public intent plus the resolved port mapping as interface metadata,
    # never the selected DUT implementation, upstream scoreboard, private traces or coverage.
    author_contract={k:v for k,v in contract.items() if k not in ('evidence','upstream_dv_corroboration','unchanged')}
    old['registered_contract_amendment']=author_contract
    old['isolation']='Public spec/interface and prior Claude source only. No DUT implementation, upstream scoreboard, calibration stimuli/traces, guards, coverage or B/C results.'
    sources={f:(PRIOR/f).read_text() for f in FILES}
    hashes=json.loads((PRIOR/'authorship.json').read_text())['artifact_sha256']
    if any(sha(PRIOR/f)!=hashes[f] for f in FILES):raise ValueError('Prior authorship drift')
    tasks=[
        'Apply only the explicitly registered byte-order correction to TX fetch, RX packing, selftests, properties and contract. Preserve byte-MSB bit order and all non-order properties.',
        'CSAAT: public theory194-209 says detected CSID/config change, not accepted change. Consider a stable valid pending offer while ready=0 as well as accepted queue. Do not treat fields with valid=0 as permission to release CS. Keep transport violations distinct.',
        'TX starvation: record trigger when an in-flight byte boundary actually lacks accepted input and pauses; record resolution and completion separately. A newly accepted word may precede the trailing resume edge, so sample-time comparison with last edge alone loses the episode. Emit pending/failed events too. Stall flags alone never prove success.',
        'Event success requires complete, correct transfer and a clean entire trigger-to-completion window, including payload faults before resolution. Preserve separate hardware/software reset and do not label unresolved software-reset obligations as proven.',
        'Legal unsupported dummy modes must be unresolved/scope unsupported, not a false driver protocol violation. Invalid speed or illegal direction stays separate. Correct supported-scope claims to evidence; never disable a meaningful checker to pass DUT observations.',
        'Selftests must exercise asymmetric payload and padding, pending CSID changes versus invalid offers, starvation with word accepted before resume sample, incomplete windows and dirty recovery windows. Keep patches concise. No private stimulus or expected output is supplied.'
    ]
    packet={'specification_and_interface':old,'prior_claude_artifacts':sources,'repair_tasks':tasks,
            'prior_artifact_sha256':hashes,'authority_contract_sha256':sha(authority/'contract.json')}
    instructions='You are Claude, the original independent SPI core specification-checker author role. A separate GPT role owns fixed driver and stimulus. Return ONLY JSON with exactly patches and rationale. patches is a list of {file,before,after}; file must be checker.py,selftest.py,properties.json or contract.md. Each before must be a nonempty UNIQUE exact substring of that prior file (apply in order). No markdown fences. Do not return whole rewritten artifacts. All expected-output changes must be authored by you and justified by public specification. No tools, RTL, simulation or coverage. The old upstream internal prose has a documented conflict; apply the registered resolution without erasing the conflict history. Keep pure Python imports collections/copy/math and check_rows API.\n'
    role=out/'packet';role.mkdir()
    write(role/'packet.json',packet);prompt=instructions+json.dumps(packet,separators=(',',':'))
    if len(prompt.encode())>150000:raise ValueError('Author packet cap')
    (role/'prompt.txt').write_text(prompt)
    write(role/'manifest.json',{'status':'prepared_not_called','packet_sha256':sha(role/'packet.json'),'prompt_sha256':sha(role/'prompt.txt'),
        'builder_sha256':sha(Path(__file__)),'bytes':len(prompt.encode()),'model':'claude-opus-5-5','calls_planned_max':2,'cli_budget_per_call_usd':4,
        'excluded':['DUT source','private calibration traces','coverage','guards','B/C results','upstream scoreboard']})
    print(json.dumps({'contract':str(authority/'contract.json'),'patch_packet_bytes':len(prompt.encode()),'B_allowed':False}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);prepare(p.parse_args().output.resolve())
