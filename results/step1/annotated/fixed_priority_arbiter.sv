//      // verilator_coverage annotation
        `timescale 1ns / 1ps
        module fixed_priority_arbiter(
 065544     input clk,                      // Clock signal
 000002     input reset,                    // Active high reset signal
 032770     input [7:0] req,                // 8-bit request signal; each bit represents a request from a different source
 000130     input [7:0] priority_override,  // External priority override signal
        
 000256     output reg [7:0] grant,         // 8-bit grant signal; only one bit will be set high based on priority
 000002     output reg valid,               // Indicates if a request is granted
 000171     output reg [2:0] grant_index    // Outputs the granted request index in binary format
        ); 
        
 065546     always @(posedge clk or posedge reset) begin
 065542         if (reset) begin
 000004             grant <= 8'b00000000;
 000004             valid <= 1'b0;
 000004             grant_index <= 3'b000;
                end 
 065542         else begin
 065281             if (priority_override != 8'b00000000) begin
 065281                 grant <= priority_override; 
 065281                 valid <= 1'b1;
 065281                 grant_index <= (priority_override[0] ? 3'd0 :
 016384                                 priority_override[1] ? 3'd1 :
 008192                                 priority_override[2] ? 3'd2 :
 004096                                 priority_override[3] ? 3'd3 :
 002048                                 priority_override[4] ? 3'd4 :
 001024                                 priority_override[5] ? 3'd5 :
 000512                                 priority_override[6] ? 3'd6 :
~000256                                 priority_override[7] ? 3'd7 : 3'd0);
                    end
 000129             else if (req[0]) begin
 000129                 grant <= 8'b00000001;
 000129                 grant_index <= 3'd0;
 000129                 valid <= 1'b1;
                    end 
 000064             else if (req[1]) begin
 000064                 grant <= 8'b00000010;
 000064                 grant_index <= 3'd1;
 000064                 valid <= 1'b1;
                    end 
 000032             else if (req[2]) begin
 000032                 grant <= 8'b00000100;
 000032                 grant_index <= 3'd2;
 000032                 valid <= 1'b1;
                    end 
 000016             else if (req[3]) begin
 000016                 grant <= 8'b00001000;
 000016                 grant_index <= 3'd3;
 000016                 valid <= 1'b1;
                    end 
 000008             else if (req[4]) begin
 000008                 grant <= 8'b00010000;
 000008                 grant_index <= 3'd4;
 000008                 valid <= 1'b1;
                    end 
 000004             else if (req[5]) begin
 000004                 grant <= 8'b00100000;
 000004                 grant_index <= 3'd5;
 000004                 valid <= 1'b1;
                    end 
 000002             else if (req[6]) begin
 000002                 grant <= 8'b01000000;
 000002                 grant_index <= 3'd6;
 000002                 valid <= 1'b1;
                    end 
 000004             else if (req[7]) begin
 000002                 grant <= 8'b10000000;
 000002                 grant_index <= 3'd7;
 000002                 valid <= 1'b1;
                    end 
 000004             else begin
 000004                 grant <= 8'b00000000;
 000004                 grant_index <= 3'd0;
 000004                 valid <= 1'b0;
                    end
                end
            end
        endmodule
