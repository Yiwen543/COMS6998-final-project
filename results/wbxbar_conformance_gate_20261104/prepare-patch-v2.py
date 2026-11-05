"""Reproducible offline preparation of three remaining ERR-boundary controls."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import patch_wbxbar_conformance_design as role
from prepare_spi_core_checker_review import vector_unpack
from prepare_wbxbar_design_revision import pack_controls
from wbxbar_checker_controls import empty_rows, settle, transfer
from run_midterm_fixed import sha

role.verify_scope()
body = json.loads((role.BASE / 'design-patch-packet-v1/packet.json').read_text())
old = body['synthetic_traces']
traces = {name: [{k: v for k, v in row.items() if k != 'action'}
                  for row in vector_unpack(packed, old['columns'])]
          for name, packed in old['values'].items()}
new = {}
rows = transfer(empty_rows(28), accept=6, forward=8, response=12, returned=13,
                addr=3, read_data=0xabcdef12)
for c in range(9, 15):
    rows[c]['pre'].update(i_mcyc=1, i_mstb=1, i_mwe=1,
                          i_maddr=5, i_mdata=0x12345678, i_msel=5, o_mstall=1)
rows[10]['pre']['o_merr'] = 1
new['err_boundary/old_live_and_held_request'] = settle(rows)
rows = empty_rows(28)
for c in range(6, 9):
    rows[c]['pre'].update(i_mcyc=1, i_mstb=1, i_mwe=1,
                          i_maddr=5, i_mdata=0x12345678, i_msel=5,
                          o_mstall=int(c < 8))
rows[8]['pre']['o_merr'] = 1
new['err_boundary/acceptance_edge'] = settle(rows)
rows = empty_rows(28)
for c in range(6, 9):
    rows[c]['pre'].update(i_mcyc=1, i_mstb=1, i_mwe=1,
                          i_maddr=5, i_mdata=0x12345678, i_msel=5, o_mstall=1)
rows[9]['pre']['o_merr'] = 1
new['err_boundary/cyc_withdrawal_edge'] = settle(rows)
traces.update(new)
if len(traces) != 91:
    raise ValueError('Historical control loss or duplicate')
parent = role.BASE / 'design-patch-v1'
body.update(previous_design=json.loads((parent / 'design.json').read_text()),
            independent_review=json.loads((parent / 'review.json').read_text()),
            synthetic_traces=pack_controls(traces), new_control_names=list(new))
body['pre_edge_event_ledgers'].update({name: role.event_ledger(rows) for name, rows in new.items()})
body['integration_cautions'] = [
    'Review R1 identifies a feasible old-live versus unaccepted-held ERR ambiguity. Preserve every source-permitted alternative, distinguish known matched slave ERR from unexplained ERR, and align the fallback counters. Do not choose a convenient owner.',
    'Review R2 may overlap existing K13 same-edge withdrawal handling. Analyze actual pre CYC and response qualification before changing anything. Its statements are questions to resolve, not an oracle. A withdrawal that keeps CYC high while withdrawing a stalled STB is a different, potentially invalid environment case; this fixture withdraws CYC.',
    'No exact starvation phase, delay or timeout precedence is documented. Do not fix a single edge with an invented grace period. State the remaining uncertainty and its effect on every touched obligation; ACK and ERR are not interchangeable.',
    'The old-live fixture keeps the held payload stable until CYC drops. If a source requires CYC to drop on every ERR, cite it and classify that fixture rather than forcing a desired label. Actual frozen driver trajectories are not supplied.',
    'The previous corrected cycle ledger remains authoritative: restart accepts6/10/14, slave acceptance16, slaveACK17, masterACK18. Do not count post changes as transfers.',
    'The clause-level unknown-tag examples predate possible_starvation_err. Make generic unknown propagation explicit so a newly named tag cannot accidentally produce scoped_pass.',
    'All 88 old cases remain unchanged. Only three new contract-development fixtures were added. No code implementation, proof certificate, DUT or B/C outcomes are present.'
]
prompt = role.AUTHOR.replace('all 81 old assessments', 'all 88 old assessments') + json.dumps(body, separators=(',', ':'))
if len(prompt.encode()) > 150000:
    raise ValueError('Author byte cap')
output = role.BASE / 'design-patch-packet-v2'
output.mkdir(parents=True, exist_ok=False)
(output / 'packet.json').write_text(json.dumps(body, indent=2) + '\n')
(output / 'prompt.txt').write_text(prompt)
paths = [role.SCOPE, Path(role.__file__), Path(__file__), parent / 'design.json', parent / 'review.json']
manifest = {'status': 'prepared_not_called', 'hashes': {str(p): sha(p) for p in paths},
            'packet_sha256': sha(output / 'packet.json'), 'prompt_sha256': sha(output / 'prompt.txt'),
            'bytes': len(prompt.encode()), 'cases': len(traces), 'new_cases': 3,
            'planned_calls_max': 2, 'cli_budget_per_call_usd': 4,
            'automatic_implementation_permission': False, 'live_B_allowed': False, 'live_C_allowed': False}
(output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
role.verify(output)
print(json.dumps(manifest, indent=2))
