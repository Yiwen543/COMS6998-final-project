#!/usr/bin/env python3
"""Build an allowlisted spec/interface-only packet for the Claude checker role."""
import argparse
import json
from pathlib import Path

from run_midterm_fixed import ROOT, sha
from run_spi_host_fixed import verify_source
from spi_host_fixture import FIELDS, OUTPUTS, COMMAND

DOC = ROOT/'third_party/opentitan_candidate/hw/ip/spi_host/doc'


def excerpt(path, ranges):
    lines = path.read_text().splitlines()
    return {'source': str(path.relative_to(ROOT)), 'sha256': sha(path),
            'excerpts': [{'start_line': a, 'end_line': b,
                          'text': '\n'.join(f'{i}: {lines[i-1]}' for i in range(a, b+1))}
                         for a, b in ranges]}


def packet():
    verify_source()
    return {
        'role': 'Independent specification/checker author, Claude; stimulus is authored by a different GPT role.',
        'scope': 'Only spi_host_fsm command/clock/control boundary, NumCS=2; no register bus, FIFO or payload data. Do not invent payload checks.',
        'authority': [excerpt(DOC/'theory_of_operation.md', [(124,145),(194,209),(213,279),(321,332),(363,377),(579,585),(641,644),(1208,1224)]),
                      excerpt(DOC/'registers.md', [(95,126),(172,248),(249,321)])],
        'interface': {
            'input_fields_widths': FIELDS, 'command_fields': list(COMMAND), 'output_fields': list(OUTPUTS),
            'input_aliases': {'rst_n': 'active-low asynchronous rst_ni', 'sw_reset': 'sw_rst_i synchronous software reset',
                'enable': 'en_i', 'valid': 'command_valid_i', 'keep_cs': 'CSAAT', 'length': 'LEN (count minus one)',
                'tx_ready': 'sr_wr_ready_i transmit source ready', 'rx_ready': 'sr_rd_ready_i receive sink ready',
                'idle': 'CSNIDLE', 'lead': 'CSNLEAD', 'trail': 'CSNTRAIL'},
            'output_aliases': {'ready': 'command_ready_o', 'wr': 'wr_en_o: load one transmit byte at rising edge',
                'rd': 'rd_en_o: deliver one receive byte at rising edge', 'last_write': 'last transmit byte indicator',
                'last_read': 'last receive byte indicator', 'sck': 'serial clock', 'csb': '2-bit active-low selects',
                'sample': 'sample_en_o', 'shift': 'shift_en_o', 'active': 'active_o',
                'tx_stall': 'tx_stall_o', 'rx_stall': 'rx_stall_o'},
            'rows': "check_rows(rows) receives [{'cycle':int,'action':{all input fields:int},'pre':{all output fields:int},'post':{all output fields:int}}].",
            'sampling': 'Inputs change with clock low; pre is settled before rising edge, post after rising edge with same inputs. Only pre handshake/control values count operations at that edge; post values may describe the NEXT operation, not a second operation. A change between previous post and current pre can result from new inputs. Each row is one core-clock cycle.',
            'transport_assumptions': 'All fields are two-state nonnegative integers of listed width. speed 0/1/2 = std/dual/quad; bidirectional legal only at std. No command valid during reset. Pending valid and command fields must hold until acceptance or reset. Treat violated assumptions separately from DUT defects. Fields when valid=0 need not hold. Initial trace starts with two reset cycles. Local LEN is 20 bits per public interface; the older prose table says 8, disclose that documentation mismatch.',
            'requested_scope_expansion': 'Allow legal queued offer of changed CSID/config while previous CSAAT segment is active; do not reuse the old project restriction requiring prior deselection. Software reset may be held until idle. Do not assume reset overcomes every possible simultaneous external stall unless supported; unresolved cases must be explicit.',
        },
        'requested_events': ['backpressure_then_recovery: a real stalled in-flight operation, release and correct resumed/completed transfer without reset',
            'abort_then_restart: in-flight transfer interrupted by software OR asynchronous reset, then a newly accepted command completes with no stale bytes; separate reset kinds',
            'constrained_transaction_switch: completed CSAAT-held segment, changed CSID or configuration offered, old selection ends, legal all-high gap and new selection/segment completes; timing based on cited spec'],
        'independence': 'No DUT source, historical checker source, calibration sequences, formal counterexamples, coverage data or B/C outcomes are in this packet. Do not infer implementation from names. Partial/unproven obligations must remain unresolved.',
    }


INSTRUCTIONS = """You are the independent specification/checker-author role in a role-separated RTL experiment.
Write a pure Python checker from the supplied public specification and interface, NOT from RTL.
Do not generate experimental stimulus or change the driver, DUT, budget, counters or experiment targets.
Return ONLY a JSON object with exactly keys checker_source, properties, contract_markdown, selftest_source.
checker_source: complete Python module defining check_rows(rows) -> dict with failures (list of cycle/category/detail),
assumption_violations (list), events (list of {family,kind,start_cycle,end_cycle,evidence}), unresolved (list),
verdict (scoped_pass/dut_violation/input_or_scope_invalid/unresolved), and counts. Include useful scope limitations.
Properties must enforce byte/last accounting, reset separation, stall safety/recovery and constrained switching at
this public-pin boundary, citing exact spec sections. Support the requested events only when fully witnessed;
an end-of-batch unfinished operation must remain pending/inconclusive, not automatically fail liveness.
Incomplete traces must not count event completion. Avoid proving success using only DUT ready/active status;
use accepted command semantics, remaining byte counts and externally observed serial/select progress.
Do not over-specify exact cycles where spec is ambiguous; mark unresolved and constrain supported scope explicitly.
When exact timing is supported use documented units and boundary observations, including old/new configuration.
If a change requires fresh idle despite CSAAT, pending command may be offered before it is accepted.
Register-bus STATUS is not necessarily identical to this direct command boundary.
properties: list of {id, requirement, source, assumption, support_status}.
contract_markdown: readable supported interface/spec contract and explicit limitations; no test vectors or target hints.
selftest_source: Python module defining run(check_rows) -> list of named test results with pass booleans.
Construct small independent hand-authored public traces, positive and single-fault controls for implemented properties.
These are hidden checker validation controls, never experimental stimulus.
Use only builtins and collections/copy/math imports, no I/O, filesystem, network, exec/eval, imports of project code,
or internal DUT signals. A controller checker may be a scoped scoreboard, but do not imply complete correctness.
Do not return Markdown fences around the JSON. Be explicit if the specification/interface cannot justify a property.
"""


def prepare(output):
    output.mkdir(parents=True, exist_ok=False)
    data = packet()
    (output/'packet.json').write_text(json.dumps(data, indent=2)+'\n')
    (output/'prompt.txt').write_text(INSTRUCTIONS+'\n\n'+json.dumps(data, separators=(',', ':'))+'\n')
    manifest = {'role': 'claude_spec_checker_author', 'source_packet_sha256': sha(output/'packet.json'),
        'prompt_sha256': sha(output/'prompt.txt'), 'builder_sha256': sha(Path(__file__)),
        'included': [x['source'] for x in data['authority']]+['public interface names, widths and sampling contract'],
        'excluded': ['RTL implementation','legacy checker source','calibration stimulus','prior model results','coverage groups'],
        'screen_config_sha256': sha(ROOT/'configs/spi_host_event_screen.json')}
    (output/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return manifest


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--output', type=Path, required=True)
    args = cli.parse_args()
    print(json.dumps(prepare(args.output.resolve()), indent=2))
