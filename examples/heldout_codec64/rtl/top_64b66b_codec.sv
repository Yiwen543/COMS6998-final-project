module top_64b66b_codec (
    // System signals
    input  logic         clk_in,
    input  logic         rst_in,
    
    // Encoder inputs
    input  logic [63:0]  enc_data_in,
    input  logic [7:0]   enc_control_in,
    
    // Encoder outputs
    output logic [65:0]  enc_data_out,
    
    // Decoder inputs
    input  logic         dec_data_valid_in,
    input  logic [65:0]  dec_data_in,
    
    // Decoder outputs
    output logic [63:0]  dec_data_out,
    output logic [7:0]   dec_control_out,
    output logic         dec_sync_error,
    output logic         dec_error_out
);

     wire [65:0] encoder_data_w;
     wire [65:0] encoder_control_data_w;



    // Instantiate the 64b/66b encoder
    encoder_data_64b66b u_encoder_data (
        .clk_in            (clk_in),
        .rst_in            (rst_in),
        .encoder_data_in   (enc_data_in),
        .encoder_control_in (enc_control_in),
        .encoder_data_out  (encoder_data_w)
    );
    
    encoder_control_64b66b u_encoder_control (
        .clk_in            (clk_in),
        .rst_in            (rst_in),
        .encoder_data_in   (enc_data_in),
        .encoder_control_in (enc_control_in),
        .encoder_data_out  (encoder_control_data_w)
    );

    // Instantiate the 64b/66b decoder
    
    decoder_data_control_64b66b u_decoder_data_control (
        .clk_in              (clk_in),
        .rst_in              (rst_in),
        .decoder_data_valid_in (dec_data_valid_in),
        .decoder_data_in     (dec_data_in),
        .decoder_data_out    (dec_data_out),
        .decoder_control_out (dec_control_out),
        .sync_error          (dec_sync_error),
        .decoder_error_out   (dec_error_out)
    );

    assign enc_data_out = (|enc_control_in) ? encoder_control_data_w : encoder_data_w;


endmodule
