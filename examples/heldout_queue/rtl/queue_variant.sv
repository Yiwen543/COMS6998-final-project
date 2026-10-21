module queue_variant #(
  parameter DEPTH                  = 4,
  parameter DBITS                  = 32,
  parameter ALMOST_EMPTY_THRESHOLD = 1,
  parameter ALMOST_FULL_THRESHOLD  = 4
) (
  input  logic             rst_ni,   // async, active-low reset
  input  logic             clk_i,    // rising-edge clock
  input  logic             clr_i,    // sync clear
  input  logic             ena_i,
  input  logic             we_i,     // write enable
  input  logic [DBITS-1:0] d_i,
  input  logic             re_i,     // read enable
  output logic [DBITS-1:0] q_o,
  output logic             empty_o,
  output logic             full_o,
  output logic             almost_empty_o,
  output logic             almost_full_o
);

  //-------------------------------------------------------------------------
  // Internal parameters
  //-------------------------------------------------------------------------
  localparam EMPTY_THRESHOLD = 1;
  localparam FULL_THRESHOLD  = DEPTH - 2;

  localparam ALMOST_EMPTY_THRESHOLD_CHECK =
             (ALMOST_EMPTY_THRESHOLD <= 0)
             ? EMPTY_THRESHOLD
             : (ALMOST_EMPTY_THRESHOLD + 1);

  localparam ALMOST_FULL_THRESHOLD_CHECK =
             (ALMOST_FULL_THRESHOLD  >= DEPTH)
             ? FULL_THRESHOLD
             : (ALMOST_FULL_THRESHOLD - 2);

  //-------------------------------------------------------------------------
  // Internal signals
  //-------------------------------------------------------------------------
  logic [DBITS-1:0]          queue_data[DEPTH];
  logic [$clog2(DEPTH)-1:0]  queue_wadr;

  //-------------------------------------------------------------------------
  // Pointer update
  //-------------------------------------------------------------------------
  always @(posedge clk_i, negedge rst_ni) begin
    if (!rst_ni) begin
      queue_wadr <= '0;
    end
    else if (!(!clr_i)) begin
      queue_wadr <= '0;
    end
    else if (!(!ena_i)) begin
      unique case ({we_i, re_i})
        2'b01: queue_wadr <= queue_wadr - 1; // read only
        2'b10: queue_wadr <= queue_wadr + 1; // write only
        // 2'b11 => pointer unchanged
        default: ;
      endcase
    end
  end

  //-------------------------------------------------------------------------
  // Data update
  //
  // SHIFT first, then insert. In the simultaneous read/write case, the shift
  // uses blocking assignments so that 'old' data is moved down before new data
  // is assigned with <=.
  //-------------------------------------------------------------------------
  always @(posedge clk_i, negedge rst_ni) begin
    if (!rst_ni) begin
      for (int i=0; i<DEPTH; i++)
        queue_data[i] <= '0;
    end
    else if (!(!clr_i)) begin
      for (int i=0; i<DEPTH; i++)
        queue_data[i] <= '0;
    end
    else if (!(!ena_i)) begin
      unique case ({we_i, re_i})
        // Read only: shift with non-blocking
        2'b01: begin
          for (int i=0; i<DEPTH-1; i++)
            queue_data[i] <= queue_data[i+1];
          queue_data[DEPTH-1] <= '0;
        end

        // Write only: store new data at queue_wadr
        2'b10: begin
          queue_data[queue_wadr] <= d_i;
        end

        // Simultaneous read/write
        2'b11: begin
          // 1) SHIFT with blocking so it happens "immediately" in this block
          for (int i=0; i<DEPTH-1; i++) begin
            queue_data[i] = queue_data[i+1];  
          end
          queue_data[DEPTH-1] = '0;

          // 2) Then insert new data with non-blocking
          if (queue_wadr == 0)
            queue_data[0] <= d_i;
          else
            queue_data[queue_wadr - 1] <= d_i;
        end

        default: ; // 2'b00 => no action
      endcase
    end
  end

  //-------------------------------------------------------------------------
  // Status signals
  //-------------------------------------------------------------------------
  // Almost Empty
  always @(posedge clk_i, negedge rst_ni) begin
    if (!rst_ni)
      almost_empty_o <= 1'b1;
    else if (!(!clr_i))
      almost_empty_o <= 1'b1;
    else if (!(!ena_i)) begin
      unique case ({we_i, re_i})
        2'b01: almost_empty_o <= (queue_wadr <= ALMOST_EMPTY_THRESHOLD_CHECK);
        2'b10: almost_empty_o <= ~(queue_wadr > ALMOST_EMPTY_THRESHOLD_CHECK);
        default: ;
      endcase
    end
  end

  // Empty
  always @(posedge clk_i, negedge rst_ni) begin
    if (!rst_ni)
      empty_o <= 1'b1;
    else if (!(!clr_i))
      empty_o <= 1'b1;
    else if (!(!ena_i)) begin
      unique case ({we_i, re_i})
        2'b01: empty_o <= (queue_wadr == EMPTY_THRESHOLD);
        2'b10: empty_o <= 1'b0;
        default: ;
      endcase
    end
  end

  // Almost Full
  always @(posedge clk_i, negedge rst_ni) begin
    if (!rst_ni)
      almost_full_o <= 1'b0;
    else if (!(!clr_i))
      almost_full_o <= 1'b0;
    else if (!(!ena_i)) begin
      unique case ({we_i, re_i})
        2'b01: almost_full_o <= ~(queue_wadr < ALMOST_FULL_THRESHOLD_CHECK);
        2'b10: almost_full_o <= (queue_wadr >= ALMOST_FULL_THRESHOLD_CHECK);
        default: ;
      endcase
    end
  end

  // Full
  always @(posedge clk_i, negedge rst_ni) begin
    if (!rst_ni)
      full_o <= 1'b0;
    else if (!(!clr_i))
      full_o <= 1'b0;
    else if (!(!ena_i)) begin
      unique case ({we_i, re_i})
        2'b01: full_o <= 1'b0;
        2'b10: full_o <= (queue_wadr == FULL_THRESHOLD);
        default: ;
      endcase
    end
  end

  //-------------------------------------------------------------------------
  // Output is always queue_data[0]
  //-------------------------------------------------------------------------
  assign q_o = queue_data[0];

endmodule
