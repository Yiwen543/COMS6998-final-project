"""Allowlisted public-spec packet; no RTL, guards, calibration or LLM outcomes."""
import argparse
import json
from pathlib import Path
from prepare_spi_checker_role import excerpt
from run_midterm_fixed import ROOT, sha
from i2c_fixture import FIELDS, OBS, TIMING

INSTRUCTIONS='''You are Claude, independent specification/checker author. GPT separately implements the driver and stimulus.
Return ONLY JSON with checker_source, selftest_source, properties, contract_markdown.
Write pure Python check_rows(rows) returning failures[{cycle,category,detail}], assumption_violations,
events[{family,kind,start_cycle,end_cycle,evidence}], unresolved, verdict, counts.
Allowed imports collections/copy/math only; no tools/I/O/network/imports of project code/exec/eval/dunder access.
Use only the supplied public spec and interface. Do NOT generate experimental stimulus or edit driver/DUT.
Implement a concise scoped write-mode wire scoreboard, reset safety, unexpected-NACK halt and recovery,
NACK timeout STOP/release. Check actual 8-bit MSB-first bytes and ACK slots plus START/STOP, not merely ready.
Important: FMT rready is a POP after processing, not initial command acceptance. Observe head while valid.
Use physical bus edges from both pre and post observations in chronological order, not synchronized scl_i.
The wire target changes ACK while SCL low. The environment launch register and input synchronizers create latency; scl_pin/sda_pin are launch register values, NOT scl_o/sda_o. Check bus wired-AND against scl_pin & !stretch and sda_pin & !target_low.
Do not impose undocumented exact core-cycle liveness; incomplete batches stay pending and cannot count success.
Successful events require a clean whole event window and complete wire byte, not DUT status alone.
Events: stretch_recovery (in-flight actual clock extension, release then correctly completed byte/STOP),
nak_restart (unexpected NACK, halted interval, software clears and a repeated START, clean new byte/STOP),
nak_timeout_recovery (unexpected NACK, timeout, automatic STOP/released idle, software clears then new byte/STOP).
Old NACK expected in an intentionally NACKing environment is an event, not a DUT defect.
Do not claim full I2C correctness. Exclude read-mode, arbitration/multicontroller, analog timings, full register bus.
properties: list of {id,requirement,source,assumption,support_status}. contract_markdown: clear scope/limitations.
selftest_source: pure module run(check_rows) -> list of {name,pass}; independent small hand traces and single faults.
Keep implementation reasonably small. Return JSON only, no Markdown fences.'''


def prepare(output):
    doc=ROOT/'third_party/opentitan_candidate/hw/ip/i2c/doc'
    packet={'role':'independent spec-only checker author', 'scope':'Pinned OpenTitan i2c_controller_fsm FifoDepth=64, write-mode only; no full IP claim.',
      'authority':[excerpt(doc/'theory_of_operation.md',[(9,120)]),excerpt(doc/'registers.md',[(462,543),(829,877)])],
      'interface':{'actions':FIELDS,'observations':list(OBS),'timing_cycles':TIMING,
       'sampling':'Each row action then pre (settled before rising core clock) then post (settled after edge). One row is one executed core cycle. Process previous post -> pre -> post physical SCL/SDA changes. pre ready&valid pops one FMT entry at this edge. Post ready is for next edge.',
       'actions_meaning':'rst_n async low reset. enable drives host_enable. push enqueues byte/start/stop/nak_ok in a fixed 64-entry FIFO before pre. Head held until pre ready&valid. flush removes entries before pre (only legal halted/idle context, caller must respect). clear_events clears sticky NACK and timeout before pre. target_ack controls external target ACK at ninth bit; stretch is external open-drain SCL pull-low. nak_timeout_enable/value drive public timeout pins. READB/RCONT fixed zero. No RX expected.',
       'observations_meaning':'scl/sda physical wired-AND bus; scl_i/sda_i two-flop synchronized bus; scl_o/sda_o release=1 drive-low=0. ready=fmt_fifo_rready_o, idle=host_idle_o; transmitting=transmitting_o. nak/nak_timeout/arbitration/scl_interference/stretch_timeout/sda_unstable/complete/rx_valid/rx_data corresponding public outputs. valid/depth/fmt_byte/fmt_start/fmt_stop/fmt_nak_ok public FMT inputs. unhandled_nak/unhandled_timeout are sticky event latches. bus_free is independent single-controller free-time monitor. target_low is external SDA pull-down; scl_pin/sda_pin are fixed environment launch-register values, visible for checking bus composition.',
       'environment':'Passive write target counts physical SCL rises between START/STOP and ACKs each ninth bit, samples target_ack during low ACK phase; no internal DUT state. It never drives logic high. Stretch only asserted while SCL low (otherwise input assumption violation). No rival controller, sda_interference fixed0. bus_free requires released bus for 6 core cycles after STOP/initial reset; no full bus monitor verification. Event latches set on pre event outputs, cleared by software action. All actions nonnegative two-state integers. Reset clears FIFO, target and sticky events; initial two reset cycles. No model can modify any of these components.'},
      'isolation':'No implementation, prior checker, source guards, private calibration or previous model results.'}
    output.mkdir(parents=True,exist_ok=False)
    (output/'packet.json').write_text(json.dumps(packet,indent=2)+'\n')
    (output/'prompt.txt').write_text(INSTRUCTIONS+'\n'+json.dumps(packet,separators=(',',':')))
    (output/'manifest.json').write_text(json.dumps({'packet_sha256':sha(output/'packet.json'),'builder_sha256':sha(Path(__file__)),
        'config_sha256':sha(ROOT/'configs/i2c_event_screen.json'),'excluded':['DUT implementation','guards','calibration','model results']},indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    prepare(p.parse_args().output.resolve())
