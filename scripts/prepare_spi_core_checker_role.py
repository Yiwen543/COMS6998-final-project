"""Allowlisted public-spec/interface packet; no RTL or experimental evidence."""
import argparse
import json
from pathlib import Path
from prepare_spi_checker_role import excerpt
from spi_core_interface import FIELDS,OUTPUTS
from real_parent_screen import configuration,verify,SCOPE
from run_midterm_fixed import ROOT,sha

INSTRUCTIONS='''You are Claude, the independent specification-checker author. A different GPT role owns the fixed JSON driver and stimulus.
Return ONLY JSON with checker_source, selftest_source, properties, contract_markdown.
checker_source defines pure Python check_rows(rows), returning failures[{cycle,category,detail}], assumption_violations,
events[{family,kind,start_cycle,end_cycle,evidence}], unresolved, verdict, counts.
Allowed imports collections/copy/math only; no tools, filesystem/network, exec/eval, project imports or dunder access.
Derive checks from the cited public specifications. Do not infer expected outputs from a DUT implementation.
Validate command and TX ready/valid transport separately from DUT defects; at a rising edge ONLY pre values handshake.
Track serial transactions, payload bytes, packing/partial-word padding, CS timing, reset/abort and recovery at the public pins.
Observe previous post -> current pre -> current post pin changes in chronological order; do not double-count transfers.
Honor Standard/Dual/Quad direction restrictions and mode/sampling distinctions. Do not invent undocumented exact-cycle deadlines.
For a software-reset during stall, do not assert stronger behavior than the specification supports; record unresolved obligations.
Successful event windows must contain the triggering event, its resolution and a correctly completed transfer with NO failures
or assumption violations in the whole window. A stall flag, ready, active=0 or accepted command alone is not completion proof.
Do not infer coverage or equivalence from event completion; do not count source points.
Incomplete batches stay pending/inconclusive, not pass or recovery success. Keep unsupported configurations explicit/blocking.
Do not weaken a checker to accommodate a DUT trace. No generated stimulus, RTL edits or coverage/experiment edits.
properties is a list of {id,requirement,source,assumptions,support_status}; contract_markdown explains exact supported scope.
selftest_source defines run(check_rows) returning [{name,pass}], using independent short hand traces and single-fault controls.
The driver author will supply further independent controls; your selftests alone will not validate the checker.
Keep the implementation concise; prefer a coherent supported scope with explicit unresolved obligations to guessed behavior.'''

def prepare(output):
    c=configuration('spi_host_core');verify(c)
    doc=ROOT/c['root']/'hw/ip/spi_host/doc/theory_of_operation.md'
    p={'role':'specification-only independent checker author',
       'scope':'Original OpenTitan spi_host_core, NumCS=2, revision '+c['revision']+'. Includes original byte merge/select, shift register and FSM. No TLUL bus, external TX/RX FIFOs, interrupt registers, electrical IO pads or passthrough.',
       'authority':[excerpt(doc,[(13,54),(91,145),(194,279),(281,320),(363,377),(579,585),(629,644),(654,675),(685,740)])],
       'interface':{'fields_widths':FIELDS,'outputs':list(OUTPUTS),
          'rows':'[{cycle:int,action:{all input fields:int},pre:{all outputs:int},post:{all outputs:int}}]',
          'aliases':{'rst_n':'rst_ni, asynchronous active-low','enable':'en_i','sw_reset':'sw_rst_i, sampled software reset',
            'valid':'command_valid_i','csid':'command_csid_i','length':'command segment LEN, byte count minus one; actual public packed port is 20 bits (older prose table says 8)',
            'keep_cs':'command segment CSAAT','speed':'0 Standard,1 Dual,2 Quad;3 reserved',
            'write/read':'command segment cmd_wr_en/cmd_rd_en; both zero dummy; bidirectional only Standard',
            'clkdiv/idle/lead/trail':'CLKDIV/CSNIDLE/CSNLEAD/CSNTRAIL, command configuration fields',
            'full_cycle/cpha/cpol':'FULLCYC/CPHA/CPOL, command configuration fields',
            'tx_data/tx_be/tx_valid':'tx_data_i[31:0], tx_be_i[3:0], tx_valid_i',
            'rx_ready':'rx_ready_i','action.sd':'sd_i[3:0], external sampled input only; no loopback is synthesized',
            'ready/tx_ready/tx_full':'command_ready_o/tx_ready_o/tx_byte_select_full_o',
            'rx_data/rx_valid':'rx_data_o[31:0]/rx_valid_o','sck/csb':'sck_o/csb_o[1:0], selects active low',
            'pre/post.sd':'sd_o[3:0]','sd_en':'sd_en_o[3:0]','rx_stall/tx_stall/active':'rx_stall_o/tx_stall_o/active_o'},
          'sampling':'Fixed 10 ns clock cycle: change inputs with clk low, pre at +4 ns, rising edge at +5 ns, post at +9 ns, falling edge at +10 ns. Before first action, initial rst_n=1 settles for 1 ns then first action asserts reset; no extra clock edge. All values are two-state integers. Initial two cycles assert reset. Subsequent six shared seed cycles are inactive.',
          'transport':'No direct access to sr_wr_ready/sr_rd_ready or internal signals. Real instantiated data path produces its own readiness. command and TX offered data must hold through backpressure until pre ready&valid or reset. No automatic handshake completion, hidden cycles or generated data. Each JSON row is exactly one clock cycle. The driver does not contain expected results.',
          'byte_order':'Core pins use already-ordered words. Per Byte Select/Merge public component contract, transmit enabled bytes and pack received bytes from most-significant toward least-significant positions. No register-window ByteOrder swapping exists in this scope.'},
       'requested_events':['tx_starvation_resume: missing input word stalls an in-flight TX operation, later word is accepted and the correct remaining payload completes without reset',
           'rx_backpressure_resume: blocked word output creates real in-flight RX backpressure, output is drained and all bytes complete without loss/duplication',
           'partial_word_then_next_transaction: short RX segment pads correctly; a held-CS next command or CSID change completes correctly',
           'reset_abort_restart: actual in-flight transfer is reset, then a fresh accepted command completes with no stale payload; distinguish hardware/software reset'],
       'isolation':'No RTL implementation, previous checkers, guard expressions, private calibration sequences, coverage data, or B/C results. Names describe public interface only.'}
    prompt=INSTRUCTIONS+'\n'+json.dumps(p,separators=(',',':'))
    if len(prompt.encode())>150000:raise ValueError('Author packet byte cap')
    output.mkdir(parents=True,exist_ok=False);(output/'packet.json').write_text(json.dumps(p,indent=2)+'\n');(output/'prompt.txt').write_text(prompt)
    (output/'manifest.json').write_text(json.dumps({'status':'prepared_not_called','bytes':len(prompt.encode()),'packet_sha256':sha(output/'packet.json'),'prompt_sha256':sha(output/'prompt.txt'),'builder_sha256':sha(Path(__file__)),'scope_sha256':sha(SCOPE),'interface_sha256':sha(ROOT/'scripts/spi_core_interface.py'),'model':'claude-opus-5-5','calls_planned_max':2,'cli_budget_per_call_usd':4,'excluded':['RTL','checker code','calibration','coverage','prior model outcomes']},indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);prepare(p.parse_args().output.resolve())
