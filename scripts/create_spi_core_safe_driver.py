"""Mechanical fixed-driver generation from the pinned old pin/clock scaffold."""
from pathlib import Path
from run_midterm_fixed import ROOT,sha
from spi_core_safe_interface import STATE
from spi_core_experiment import verify_freeze

def create():
    verify_freeze()
    old=ROOT/'examples/spi_core_integration/verif/tb_spi_core.sv'
    out=ROOT/'examples/spi_core_integration/verif/tb_spi_core_safe.sv'
    if out.exists():raise FileExistsError(out)
    body=old.read_text();header,rest=body.split('initial begin',1)
    header=header.replace('// Fixed public-input replay; no expected DUT outputs or hierarchical drives.',
        '// Offer-per-cycle driver. Public ready only; no expected DUT outputs or internal drives.')
    header=header.replace('v_valid','v_cmd_offer').replace('v_tx_valid','v_tx_offer')
    init=rest.split('while(!$feof(fd)) begin',1)[0]
    scan=body.split('got=$fscanf',1)[1].split('if(got==22)',1)[0]
    scan='got=$fscanf'+scan.replace('v_valid','v_cmd_offer').replace('v_tx_valid','v_tx_offer')
    payload=body.split('command_i.segment.speed=v_speed',1)[1].split('tx_data_i=v_tx_data',1)[0]
    payload='command_i.segment.speed=v_speed'+payload
    payload=payload.replace('command_i.','incoming.')
    decl='''
localparam integer Capacity=392;
command_t incoming;
command_t cmd_mem [0:Capacity-1];
reg csid_mem [0:Capacity-1];
reg [31:0] tx_mem [0:Capacity-1];
reg [3:0] be_mem [0:Capacity-1];
integer cmd_ids [0:Capacity-1];
integer tx_ids [0:Capacity-1];
integer ch=0,ct=0,th=0,tt=0;
integer cmd_added,tx_added,cmd_taken,tx_taken;
integer cmd_offered=0,tx_offered=0,cmd_accepted=0,tx_accepted=0,cmd_cancelled=0,tx_cancelled=0;
reg cmd_fire,tx_fire;
'''
    logic='''
if(cycle>=Capacity) $fatal(1,"Physical cycle cap");
rst_ni=v_rst_n[0];en_i=v_enable[0];sw_rst_i=v_sw_reset[0];
rx_ready_i=v_rx_ready[0];sd_i=v_sd[3:0];
cmd_added=-1;tx_added=-1;cmd_taken=-1;tx_taken=-1;
if(!rst_ni) begin
  if(v_cmd_offer || v_tx_offer) $fatal(1,"Offer during reset");
  cmd_cancelled=cmd_cancelled+ct-ch;tx_cancelled=tx_cancelled+tt-th;
  ch=0;ct=0;th=0;tt=0;
  command_i='0;command_csid_i=0;tx_data_i=0;tx_be_i=0;
end else begin
  if(v_cmd_offer) begin
    if(ct>=Capacity) $fatal(1,"Command queue overflow");
PAYLOAD
    cmd_mem[ct]=incoming;csid_mem[ct]=v_csid[0];cmd_ids[ct]=cycle;
    ct=ct+1;cmd_offered=cmd_offered+1;cmd_added=cycle;
  end
  if(v_tx_offer) begin
    if(tt>=Capacity) $fatal(1,"TX queue overflow");
    tx_mem[tt]=v_tx_data;be_mem[tt]=v_tx_be[3:0];tx_ids[tt]=cycle;
    tt=tt+1;tx_offered=tx_offered+1;tx_added=cycle;
  end
end
command_valid_i=(ct>ch);tx_valid_i=(tt>th);
if(command_valid_i) begin command_i=cmd_mem[ch];command_csid_i=csid_mem[ch];end
if(tx_valid_i) begin tx_data_i=tx_mem[th];tx_be_i=be_mem[th];end
#4;
cmd_fire=command_valid_i && command_ready_o;
tx_fire=tx_valid_i && tx_ready_o;
'''.replace('PAYLOAD',payload)
    pins=['rst_ni','en_i','sw_rst_i','command_valid_i','command_csid_i','command_i.segment.speed',
        'command_i.segment.cmd_wr_en','command_i.segment.cmd_rd_en','command_i.segment.len','command_i.segment.csaat',
        'command_i.configopts.clkdiv','command_i.configopts.csnidle','command_i.configopts.csnlead',
        'command_i.configopts.csntrail','command_i.configopts.full_cyc','command_i.configopts.cpha','command_i.configopts.cpol',
        'tx_data_i','tx_be_i','tx_valid_i','rx_ready_i','sd_i']
    outputs=['command_ready_o','tx_ready_o','tx_byte_select_full_o','rx_data_o','rx_valid_o','sck_o','csb_o',
             'sd_o','sd_en_o','rx_stall_o','tx_stall_o','active_o']
    trace='$write("TRACE '+' '.join(['%0d']*(1+len(pins)+len(outputs)))+'",'+','.join(['cycle']+pins+outputs)+');\n'
    trace+='#1;clk_i=1;#4;\n$display(" '+' '.join(['%0d']*len(outputs))+'",'+','.join(outputs)+');\n'
    tail='''
if(cmd_fire) begin cmd_taken=cmd_ids[ch];ch=ch+1;cmd_accepted=cmd_accepted+1;end
if(tx_fire) begin tx_taken=tx_ids[th];th=th+1;tx_accepted=tx_accepted+1;end
if(cmd_offered!=cmd_accepted+cmd_cancelled+ct-ch) $fatal(1,"Command conservation");
if(tx_offered!=tx_accepted+tx_cancelled+tt-th) $fatal(1,"TX conservation");
'''
    tail+='$display("QUEUE '+' '.join(['%0d']*len(STATE))+'",cycle,cmd_added,tx_added,cmd_taken,tx_taken,ct-ch,tt-th,cmd_offered,tx_offered,cmd_accepted,tx_accepted,cmd_cancelled,tx_cancelled);\n'
    tail+='''#1;clk_i=0;cycle=cycle+1;
end else if(got!=-1) $fatal(1,"Malformed vectors");
end
$fclose(fd);$display("DRIVER_OK steps=%0d",cycle);$finish;
end
endmodule
'''
    out.write_text(header+decl+'initial begin'+init+'while(!$feof(fd)) begin\n'+scan+'if(got==22) begin\n'+logic+trace+tail)
    print(str(out.relative_to(ROOT)),sha(out))

if __name__=='__main__':create()
