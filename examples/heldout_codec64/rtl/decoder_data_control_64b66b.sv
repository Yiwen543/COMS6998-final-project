module decoder_data_control_64b66b (
    input  logic         clk_in,              // Clock signal
    input  logic         rst_in,              // Asynchronous reset (active high)
    input  logic         decoder_data_valid_in, // Input data valid signal
    input  logic [65:0]  decoder_data_in,     // 66-bit encoded input
    output logic [63:0]  decoder_data_out,    // Decoded 64-bit data output
    output logic [7:0]   decoder_control_out, // Decoded 8-bit control output
    output logic         sync_error,          // Sync error flag
    output logic         decoder_error_out    // Type field error flag
);

    logic [1:0] sync_header;
    logic [7:0] type_field;
    logic [55:0] data_in;
    logic type_field_valid;
    logic decoder_wrong_ctrl_received;
    logic decoder_wrong_type_field;

    `ifndef BUG_5
    assign sync_header = decoder_data_in[65:64];
    assign type_field = decoder_data_in[63:56];
    assign data_in = decoder_data_in[55:0];
    `else
    assign sync_header = decoder_data_in[10:9];
    assign type_field = decoder_data_in[7:0];
    assign data_in = decoder_data_in[63:8];
    `endif

    always_comb begin
        type_field_valid = 1'b0;
        if (sync_header == 2'b10) begin
            case (type_field)
                8'h1E, 8'h33, 8'h78, 8'h87, 8'h99, 8'hAA, 8'hB4, 
                8'hCC, 8'hD2, 8'hE1, 8'hFF, 8'h2D, 8'h4B, 8'h55, 8'h66: 
                    type_field_valid = 1'b1;
                default: type_field_valid = 1'b0;
            endcase
        end
    end

    always_ff @(posedge clk_in or posedge rst_in) begin
        if (rst_in) begin
            decoder_control_out <= 8'b0;
        end 
        else if (decoder_data_valid_in) begin
            if (sync_header == 2'b10) begin
                case (type_field)
                    8'h1E: decoder_control_out <= 8'b11111111;
                    8'h33: decoder_control_out <= 8'b00011111;
                    8'h78: decoder_control_out <= 8'b00000001;
                    8'h87: decoder_control_out <= 8'b11111110;
                    8'h99: decoder_control_out <= 8'b11111110;
                    8'hAA: decoder_control_out <= 8'b11111100;
                    8'hB4: decoder_control_out <= 8'b11111000;
                    8'hCC: decoder_control_out <= 8'b11110000;
                    8'hD2: decoder_control_out <= 8'b11100000;
                    8'hE1: decoder_control_out <= 8'b11000000;
                    8'hFF: decoder_control_out <= 8'b10000000;
                    8'h2D: decoder_control_out <= 8'b00011111;
                    8'h4B: decoder_control_out <= 8'b11110001;
                    8'h55: decoder_control_out <= 8'b00010001;
                    8'h66: decoder_control_out <= 8'b00010001;
                    default: decoder_control_out <= 8'b0;
                endcase
            end
            else begin
                decoder_control_out <= 8'b0;
            end
        end
    end

    always_ff @(posedge clk_in or posedge rst_in) begin
        if (rst_in) begin
            decoder_data_out <= 64'b0;
        end 
        else if (decoder_data_valid_in) begin
                    case (type_field)
	             `ifndef BUG_6
                        8'h1E: if (data_in[55:0] == {8{7'h1E}}) decoder_data_out <= {8{8'hFE}};
                               else decoder_data_out <= {8{8'h07}};
                        8'h33: decoder_data_out <= {data_in[55:32], 8'hFB, {4{8'h07}}};
                        8'h78: decoder_data_out <= {data_in[55:0], 8'hFB};
                        8'h87: decoder_data_out <= {{7{8'h07}},8'hFD};
                        8'h99: decoder_data_out <= {{6{8'h07}}, 8'hFD, data_in[7:0]};
                        8'hAA: decoder_data_out <= {{5{8'h07}}, 8'hFD, data_in[15:0]};
                        8'hB4: decoder_data_out <= {{4{8'h07}}, 8'hFD, data_in[23:0]};
		     `else
                        8'h1E: if (data_in[55:0] == {8{7'hEE}}) decoder_data_out <= {8{8'hEF}};
                               else decoder_data_out <= {8{8'h77}};
                        8'h33: decoder_data_out <= {data_in[23:0], 8'hFA, {4{8'h01}}};
                        8'h78: decoder_data_out <= {data_in[55:0], 8'hFA};
                        8'h87: decoder_data_out <= {{7{8'h17}},8'hFE};
                        8'h99: decoder_data_out <= {{6{8'h00}}, 8'hFD, data_in[23:16]};
                        8'hAA: decoder_data_out <= {{5{8'hFF}}, 8'hFD, data_in[15:0]};
                        8'hB4: decoder_data_out <= {{4{8'hE7}}, 8'h0D, data_in[23:0]};
		     `endif
                        8'hCC: decoder_data_out <= {{3{8'h07}}, 8'hFD, data_in[31:0]};
                        8'hD2: decoder_data_out <= {{2{8'h07}}, 8'hFD, data_in[39:0]};
                        8'hE1: decoder_data_out <= {8'h07, 8'hFD, data_in[47:0]};
	             `ifndef BUG_7
                        8'hFF: decoder_data_out <= {8'hFD, data_in[55:0]};
                        8'h2D: decoder_data_out <= {data_in[55:32], 8'h9C, {4{8'h07}}};
                        8'h4B: decoder_data_out <= {{4{8'h07}}, data_in[28:5], 8'h9C};
                        8'h55: decoder_data_out <= {data_in[55:32], 8'h9C, data_in[23:0], 8'h9C};
                        8'h66: decoder_data_out <= {data_in[55:32], 8'hFB, data_in[23:0], 8'h9C};
		     `else
                        8'hFF: decoder_data_out <= {8'hFA, data_in[55:0]};
                        8'h2D: decoder_data_out <= {data_in[55:32], 8'h00, {4{8'h07}}};
                        8'h4B: decoder_data_out <= {{4{8'h07}}, data_in[28:5], 8'h91};
                        8'h55: decoder_data_out <= {data_in[55:32], 8'h9A, data_in[23:0], 8'hCC};
                        8'h66: decoder_data_out <= {data_in[55:32], 8'hFF, data_in[23:0], 8'hED};
		     `endif
                        default: decoder_data_out <= 64'b0;
                    endcase
        end
    end

    always_ff @(posedge clk_in or posedge rst_in) begin
        if (rst_in) begin
            sync_error <= 1'b0;
        end 
        else if (decoder_data_valid_in) begin
	 `ifndef BUG_8
            sync_error <= (sync_header != 2'b01 && sync_header != 2'b10);
         `else
            sync_error <= (sync_header != 2'b00 && sync_header != 2'b11);
         `endif
        end
    end

    always_ff @(posedge clk_in or posedge rst_in) begin
        if (rst_in) begin
            decoder_wrong_type_field <= 1'b0;
        end 
        else if (decoder_data_valid_in) begin
            if (sync_header == 2'b10) begin
                decoder_wrong_type_field <= ~type_field_valid;
            end
            else begin
                decoder_wrong_type_field <= 1'b0;
            end
        end
    end
    
    assign decoder_error_out = decoder_wrong_ctrl_received || decoder_wrong_type_field;

    always_ff @(posedge clk_in or posedge rst_in) begin
        if (rst_in) begin
            decoder_wrong_ctrl_received <= 1'b0;
        end 
        else if (decoder_data_valid_in) begin
            if (sync_header == 2'b10) begin
                case (type_field)
	 `ifndef BUG_9
                    8'h1E: if ((data_in[55:0] == {8{7'h1E}}) || (data_in[55:0] == {8{7'h00}})) decoder_wrong_ctrl_received <= 1'b0;
                           else decoder_wrong_ctrl_received <= 1'b1;
                    8'h33: if (data_in [31:0] != 32'd0) decoder_wrong_ctrl_received <= 1'b1;
                           else decoder_wrong_ctrl_received <= 1'b0;
                    8'h87: if (data_in [55:0] != 56'd0) decoder_wrong_ctrl_received <= 1'b1;
                           else decoder_wrong_ctrl_received <= 1'b0;
                    8'h99: if (data_in [55:8] != 48'd0) decoder_wrong_ctrl_received <= 1'b1;
                           else decoder_wrong_ctrl_received <= 1'b0;
                    8'hAA: if (data_in [55:16] != 40'd0) decoder_wrong_ctrl_received <= 1'b1;
                           else decoder_wrong_ctrl_received <= 1'b0;
         `else
                    8'h1E: if ((data_in[55:0] == {8{7'h1E}}) || (data_in[55:0] == {8{7'h00}})) decoder_wrong_ctrl_received <= 1'b1;
                           else decoder_wrong_ctrl_received <= 1'b0;
                    8'h33: if (data_in [31:0] != 32'd0) decoder_wrong_ctrl_received <= 1'b0;
                           else decoder_wrong_ctrl_received <= 1'b1;
                    8'h87: if (data_in [55:0] != 56'd0) decoder_wrong_ctrl_received <= 1'b0;
                           else decoder_wrong_ctrl_received <= 1'b1;
                    8'h99: if (data_in [55:8] != 48'd0) decoder_wrong_ctrl_received <= 1'b0;
                           else decoder_wrong_ctrl_received <= 1'b1;
                    8'hAA: if (data_in [55:16] != 40'd0) decoder_wrong_ctrl_received <= 1'b0;
                           else decoder_wrong_ctrl_received <= 1'b1;
         `endif
                    8'hB4: if (data_in [55:24] != 32'd0) decoder_wrong_ctrl_received <= 1'b1;
                           else decoder_wrong_ctrl_received <= 1'b0;
                    8'hCC: if (data_in [55:32] != 24'd0) decoder_wrong_ctrl_received <= 1'b1;
                           else decoder_wrong_ctrl_received <= 1'b0;
                    8'hD2: if (data_in [55:40] != 16'd0) decoder_wrong_ctrl_received <= 1'b1;
                           else decoder_wrong_ctrl_received <= 1'b0;
                    8'hE1: if (data_in [55:48] != 8'd0) decoder_wrong_ctrl_received <= 1'b1;
                           else decoder_wrong_ctrl_received <= 1'b0;
                    8'h2D: if (data_in [31:0] != 32'hF0000000) decoder_wrong_ctrl_received <= 1'b1;
                           else decoder_wrong_ctrl_received <= 1'b0;
                    8'h4B: if (data_in[55:28] != {4{7'h00}} && data_in[3:0] != 4'b1111) decoder_wrong_ctrl_received <= 1'b1;
                           else decoder_wrong_ctrl_received <= 1'b0;              
                    8'h55: if (data_in[31:24] != 8'hFF) decoder_wrong_ctrl_received <= 1'b1;
                           else decoder_wrong_ctrl_received <= 1'b0; 
                    8'h66: if (data_in[31:24] != 8'h0F) decoder_wrong_ctrl_received <= 1'b1;
                           else decoder_wrong_ctrl_received <= 1'b0; 
                    default: decoder_wrong_ctrl_received <= 1'b0; 
                endcase
            end
            else begin
                decoder_wrong_ctrl_received <= 1'b0;
            end
        end
    end

endmodule
