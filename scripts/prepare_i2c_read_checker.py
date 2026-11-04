"""Public-spec-only independent READB checker author packet, no DUT source."""
import argparse
import json
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from prepare_spi_checker_role import excerpt
from i2c_read_fixture import FIELDS,OBS,TIMING

INSTRUCTIONS='''You are Claude, independent specification/checker author. GPT implements the environment and stimulus separately.
Write a new pure Python scoped read/write I2C checker. Return ONLY JSON with exactly
checker_source, selftest_source, properties, contract_markdown. No tools or code execution.
checker_source defines check_rows(rows) returning failures[{cycle,category,detail}], assumption_violations,
events[{family,kind,start_cycle,end_cycle,evidence}], unresolved, verdict(pass/fail/pending/invalid), counts.
selftest_source defines run(check_rows)->[{name,pass}]. Only builtins and collections/copy/math imports.
No I/O/network/project imports/exec/eval/dunder access. Do not generate model stimulus or change the driver.
Derive requirements from cited public specification. Use public pins, queued FMT commands and decoded wire bytes;
do not use internal RTL or hardcoded state machine cycles. Check actual data, ACK/NACK, READB length,
RCONT chaining, RX byte ordering/count, START/STOP, FIFO pop-after-processing, reset separating transactions.
Useful sampling cautions: rready is a POP after processing, NOT initial acceptance. RX may be delivered
after eight data bits and before the ninth ACK. Do not require RX to wait for ACK. Match RX against decoded
eight-bit wire bytes, separately check ninth-bit ACK/NACK. A STOP/reSTART setup rise after a ninth bit is
not a data byte; discard a pending setup bit at START/STOP. Never silently discard a full data byte.
Exactly one RX per read wire byte. When an entry completes/pops, missing/extra RX is a failure. Incomplete
trace is pending; never enforce an invented liveness deadline. FBYTE0 means256, not zero/no-op.
For read commands ignore START flag per spec; RCONT=1 ACKs the final read byte; otherwise final byte NACK,
intermediate bytes ACK. Read command FBYTE is a count, not a wire byte or slave address.
Track command identities independent of pop; a repeated START starts an address WRITE then READB commands.
Events: multi_byte_read (one READB>=2 fully delivered, correct intermediate/final ACK, STOP),
rcont_chain (>=2 READB entries chained with RCONT ACK at boundary, final NACK and STOP),
read_then_restart (complete read terminated by NACK, no STOP, repeated START and new correctly
completed address/transaction ending STOP), read_stretch_recovery (actual target extension during a read,
release, correct RX and final ACK/NACK+STOP). Use the whole trace clean gate as well as inclusive event
windows: faults/assumptions at the origin cycle invalidate success. Partial event must never receive credit.
Keep properties scoped: ACKing external target, no arbitration, no NACK error recovery required in this profile,
no analog/exact-cycle timing or timeout proof. If unexpected bus/halt error occurs mark unsupported/pending
unless a supported property is violated; do not silently treat it as pass. Do not claim all-IP correctness.
Include positive and negative selftests for RX corruption/duplicate/missing, ACK polarity, RCONT boundary,
FBYTE0 truncation, premature pop, reset and incomplete event. Keep implementation focused and reasonably small.
properties is a list of {id,requirement,source,assumption,support_status}. contract_markdown states limits.
Output JSON only, no Markdown fences.'''


def prepare(out):
    doc=ROOT/'third_party/opentitan_candidate/hw/ip/i2c/doc'
    packet={'role':'independent Claude specification checker author; separate from GPT driver/stimulus',
      'scope':'OpenTitan controller FifoDepth64, READB plus address/data writes, single controller and ACKing external target',
      'authority':[excerpt(doc/'theory_of_operation.md',[(9,87)]),excerpt(doc/'registers.md',[(273,331),(462,543)])],
      'interface':{'action_widths':FIELDS,'observation_fields':OBS,'timing':TIMING,
      'action_semantics':'push enqueues byte, start, stop, nak_ok, read, rcont. Stable FIFO head until pre valid&ready pops. read/rcont correspond READB/RCONT. target_data sets external read transmitter byte (latched at entry to each physical read byte, not a DUT expectation). target_ack ACKs writes/address. rst_n async low; enable,flush,clear_events,stretch,timeout fields as named. Host enable and target_ack normally1. No RX backpressure input exists; RX sink accepts every pre rx_valid at core rising edge.',
      'observations':'ready=FMT pop, valid/depth/fmt_* reflect FIFO head. rx_valid/rx_data public RX output. scl/sda physical bus; scl_i/sda_i two-flop input sync; scl_o/sda_o combinational controller release signals; scl_pin/sda_pin environmental launch-register release values. Bus scl=scl_pin & !stretch, sda=sda_pin & !target_low. Remaining outputs are public controller idle/transmitting/events. No internal DUT state observed.',
      'sampling':'Each row cycle, action, pre, post. Apply action while core clocklow; pre settled before rising edge, post settled after. Only pre valid/ready or pre rx_valid counts edge transfers. Inspect previous post -> pre -> post for physical wire edges. Multiple core rows per serial bit; never double-count post rx_valid.',
      'target':'Passive target decodes first 8 bits after each START as address; LSB1 selects read after ACK. MSB-first target_data transmitted perbyte, SDA released for ninth controller ACK. ACK continues data, NACK releases until next START/STOP. Target operates only on physical pins. Stretch starts only when SCL low. No read internals feed back to target.',
      'legal_inputs':'All integer two-state fields of stated widths; initial two reset cycles. READB+NAKOK and READB+RCONT+STOP rejected. Clear/flush only legal idle/halted environment. READB follows read-address WRITE, no automatic missing-address insertion. Reset clears queue and target. Untimed physical data changes only while SCLlow except START/STOP.',
      'boundary':'One output launch register and two input synchronizers are fixed environment. No exact core-cycle RX timing is specified beyond byte/command causality. Counter denominator and driver cannot be modified by author.'},
      'isolation':'No DUT code, original checker, calibration vectors, guards, model outcomes or coverage data.'}
    out.mkdir(parents=True,exist_ok=False)
    (out/'packet.json').write_text(json.dumps(packet,indent=2)+'\n')
    (out/'prompt.txt').write_text(INSTRUCTIONS+'\n'+json.dumps(packet,separators=(',',':')))
    (out/'manifest.json').write_text(json.dumps({'source_packet_sha256':sha(out/'packet.json'),
        'prompt_sha256':sha(out/'prompt.txt'),'config_sha256':sha(ROOT/'configs/i2c_read_screen.json'),
        'builder_sha256':sha(Path(__file__))},indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);prepare(p.parse_args().output.resolve())
