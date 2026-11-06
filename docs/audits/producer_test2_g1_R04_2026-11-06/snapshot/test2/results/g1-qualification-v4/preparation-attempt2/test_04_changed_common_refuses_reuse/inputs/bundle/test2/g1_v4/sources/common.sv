`timescale 1ns/1ps
// Public language controls, not a DUT specification oracle.
module stimulus(input wire [2:0] step, output reg [3:0] a,b,
                output reg rst,en,valid);
  always @* begin
    a=4'd0; b=4'd0; rst=1'b0; en=1'b0; valid=1'b0;
    case(step)
      3'd0: begin a=4'd0; b=4'd0; rst=1'b1; end
      3'd1: begin a=4'd15; b=4'd1; en=1'b1; valid=1'b1; end
      3'd2: begin a=4'd8; b=4'd1; en=1'b1; valid=1'b1; end
      3'd3: begin a=4'd1; b=4'd2; en=1'b1; valid=1'b1; end
      default: begin end
    endcase
  end
endmodule

module control #(parameter integer ID=0)(input wire clk,rst,en,valid,
  input wire [2:0] step, input wire [3:0] a,b,
  output reg [3:0] q, output reg active,ok);
  wire [4:0] full5={1'b0,a}+{1'b0,b};
  wire [3:0] sum4=a+b;
  wire signed [3:0] signed_a=$signed(a);
  wire [3:0] expected_pre=(step<=3'd1)?4'd0:({1'b0,step}-4'd1);
  wire [3:0] expected_post={1'b0,step};
  wire [3:0] literal_x=4'bx001;
  initial q=4'd0;
  generate if(ID==11) begin: altered_reset
    always @(posedge clk) if(!rst) q<=4'd0; else if(en) q<=q+4'd1;
  end else begin: registered_reset
    always @(posedge clk) if(rst) q<=4'd0; else if(en) q<=q+4'd1;
  end endgenerate
  always @* begin
    active=valid && en && !rst; ok=1'b1;
    case(ID)
      0: ok=(a==a);
      1: ok=1'b0;
      2: ok=(sum4==full5[3:0]);
      3: ok=({1'b0,sum4}==full5);
      4: ok=((signed_a<4'sd0)==a[3]);
      5: ok=(($unsigned(a)<4'd0)==a[3]);
      6: begin active=valid && en && !rst && (a!=4'd0); ok=(a!=4'd0); end
      7: begin active=1'b0; ok=1'b0; end
      8: ok=(q==expected_pre);
      9: ok=(q==expected_post);
      10: begin active=(step<3'd4); ok=(q==expected_pre); end
      11: begin active=(step>=3'd2)&&(step<3'd4); ok=(q==expected_pre); end
      12: ok=(literal_x==4'b0001);
      13: ok=((^literal_x)===1'bx);
      14: ok=1'b1;
      15: begin active=1'b0; ok=1'b1; end
      default: begin active=1'b0; ok=1'b0; end
    endcase
  end
endmodule

// SYNTHETIC_DRIFT
