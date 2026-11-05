`line 1 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 1
 

`line 3 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
 
 
 

`line 7 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
 
 
 
 
 
 
 
 

`line 16 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
 

`line 18 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
 
 
 

`line 22 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
 
 
 
 

`line 27 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
 
 
 
 
 
 
 
 
 
 

`line 38 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
 
 
 
 
 

`line 44 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
 
 
 

`line 48 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
 
 

`line 51 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
 
 
 
 
 
 

`line 58 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
 
 
 
 
 

`line 64 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
 
 
 
 
 
 
 
 
 
 
 
 

`line 77 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
 

`line 79 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
`default_nettype none
 
module skidbuffer #(
		 
		parameter	[0:0]	OPT_LOWPOWER = 0,
		parameter	[0:0]	OPT_OUTREG = 1,
		
		parameter	[0:0]	OPT_PASSTHROUGH = 0,
		parameter		DW = 8,
		parameter	[0:0]	OPT_INITIAL = 1'b1
		 
	) (
		 
		input	wire			i_clk, i_reset,
		input	wire			i_valid,
		output	wire			o_ready,
		input	wire	[DW-1:0]	i_data,
		output	wire			o_valid,
		input	wire			i_ready,
		output	reg	[DW-1:0]	o_data
		 
	);

`line 102 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
	wire	[DW-1:0]	w_data;

`line 104 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
	generate if (OPT_PASSTHROUGH)
	begin : PASSTHROUGH
		 
		assign	{ o_valid, o_ready } = { i_valid, i_ready };

`line 109 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		always @(*)
		if (!i_valid && OPT_LOWPOWER)
			o_data = 0;
		else
			o_data = i_data;

`line 115 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		assign	w_data = 0;

`line 117 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		 
		/*verilator lint_off UNUSED*/
		 
		wire	unused_passthrough;
		assign	unused_passthrough = &{ 1'b0, i_clk, i_reset };
		 
		/*verilator lint_on UNUSED*/
		 
	end else begin : LOGIC
		 
		 
		reg			r_valid;
		reg	[DW-1:0]	r_data;

`line 131 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		 
		 
		initial if (OPT_INITIAL) r_valid = 0;
		always @(posedge i_clk)
		if (i_reset)
			r_valid <= 0;
		else if ((i_valid && o_ready) && (o_valid && !i_ready))
			 
			r_valid <= 1;
		else if (i_ready)
			r_valid <= 0;
		 

`line 144 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		 
		 
		initial if (OPT_INITIAL) r_data = 0;
		always @(posedge i_clk)
		if (OPT_LOWPOWER && i_reset)
			r_data <= 0;
		else if (OPT_LOWPOWER && (!o_valid || i_ready))
			r_data <= 0;
		else if ((!OPT_LOWPOWER || !OPT_OUTREG || i_valid) && o_ready)
			r_data <= i_data;

`line 155 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		assign	w_data = r_data;
		 

`line 158 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		 
		 
		assign o_ready = !r_valid;
		 

`line 163 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		
		 
		
		if (!OPT_OUTREG)
		begin : NET_OUTPUT
			 
			 
			 
			 
			assign	o_valid = !i_reset && (i_valid || r_valid);
			 

`line 175 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
			 
			 
			always @(*)
			if (r_valid)
				o_data = r_data;
			else if (!OPT_LOWPOWER || i_valid)
				o_data = i_data;
			else
				o_data = 0;
			 
			 
		end else begin : REG_OUTPUT
			 
			 
			 
			 
			reg	ro_valid;

`line 193 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
			initial if (OPT_INITIAL) ro_valid = 0;
			always @(posedge i_clk)
			if (i_reset)
				ro_valid <= 0;
			else if (!o_valid || i_ready)
				ro_valid <= (i_valid || r_valid);

`line 200 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
			assign	o_valid = ro_valid;
			 

`line 203 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
			 
			 
			initial if (OPT_INITIAL) o_data = 0;
			always @(posedge i_clk)
			if (OPT_LOWPOWER && i_reset)
				o_data <= 0;
			else if (!o_valid || i_ready)
			begin

`line 212 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
				if (r_valid)
					o_data <= r_data;
				else if (!OPT_LOWPOWER || i_valid)
					o_data <= i_data;
				else
					o_data <= 0;
			end
			 

`line 221 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
			 
		end
		 
	end endgenerate

`line 226 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
	 
	 
	/*verilator coverage_off*/
	/*verilator lint_off UNUSED*/
	wire	unused;
	assign	unused = &{ 1'b0, w_data };
	/*verilator lint_on UNUSED*/
	/*verilator coverage_on*/
	 
 
 
 

`line 239 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
 
 
 
 
 
	
	
	

`line 248 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
	


`line 251 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		

`line 253 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		  
	  
		  

`line 257 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
	 
	 
		

`line 261 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
	
	
	
	
	
	
	  
	 
	
		  
	         
		  

`line 274 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
	
	
	
	 
		    
	

`line 281 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
	 
		    
		      
	

`line 286 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
	
		 

`line 289 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		 


`line 292 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
	
	
	
	
	
	
	

`line 300 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
	  
	

`line 303 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		  
		  
		
			
			  
		         
			
			
			  

`line 313 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
	 
	
	
	
	
	
	
	
	
	  
	
		
		
		
		
		  
		     
			
		

`line 333 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		
		
		
		
	
		  
		       
			     
			    

`line 343 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		   
			  
			  
				     
				     

`line 349 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		

`line 351 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		
		
		
		 
		
			
			  
			     
					 
			
				  
				    
			
			
		  
			
			  
			   
			
				   
					

`line 373 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
				     
					
			
			
		
		

`line 380 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		
		
		
		  
		     
			
		

`line 388 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		
		
		
		 
		
			 
			     
				  

`line 397 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
			 
			 
				  

`line 401 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		
		
	 
	

`line 406 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
	  
	     
		

`line 410 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
	
	
	
	
	
	
	
	
	  
	
			

`line 422 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
			  
		  
		 
			  
		      
		
			     
				  
		       
			  


`line 434 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
	
				 

`line 437 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		  
		 
		
			  
			   
		  
			    
			      
			
			     
				  
			     
				  
			     
				  
			     
				  
			      
				  
			     
				  
			     
				  
			      
				  
			      
				  
			     
				  
			    
				  
			    
				  
			 
				  
				    
				   
					  
				
					    
				
			 
			
		


`line 483 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
		
		   
			  
			  
			     
			   
			     
			    
			     
			
			    
			     

`line 496 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
	 
	
	

`line 500 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
 
endmodule

`line 503 "third_party/wb2axip_candidate/rtl/skidbuffer.v" 0
`line 1 "third_party/wb2axip_candidate/rtl/addrdecode.v" 1
 

`line 3 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
 
 
 

`line 7 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
 
 
 
 
 
 
 

`line 15 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
 
 

`line 18 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
 
 
 

`line 22 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
 
 

`line 25 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
 
 
 

`line 29 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
 
 
 
 
 
 
 
 
 


`line 40 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
 
 

`line 43 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
 
 
 
 
 

`line 49 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
 
 
 
 
 
 
 
 
 
 
 
 

`line 62 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
 

`line 64 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
`default_nettype	none
 
module	addrdecode #(
		 
		parameter	NS=8,
		parameter	AW = 32, DW=32+32/8+1+1,
		
		 
		 
		parameter	[NS*AW-1:0]	SLAVE_ADDR = {
				{ 3'b111,  {(AW-3){1'b0}} },
				{ 3'b110,  {(AW-3){1'b0}} },
				{ 3'b101,  {(AW-3){1'b0}} },
				{ 3'b100,  {(AW-3){1'b0}} },
				{ 3'b011,  {(AW-3){1'b0}} },
				{ 3'b010,  {(AW-3){1'b0}} },
				{ 4'b0010, {(AW-4){1'b0}} },
				{ 4'b0000, {(AW-4){1'b0}} }},
		
		 
		 
		 
		parameter	[NS*AW-1:0]	SLAVE_MASK = (NS <= 1) ? 0
			: { {(NS-2){ 3'b111, {(AW-3){1'b0}} }},
				{(2){ 4'b1111, {(AW-4){1'b0}} }} },
		
		 
		 
		 
		 
		 
		 
		 
		 
		parameter	[NS-1:0]	ACCESS_ALLOWED = -1,
		
		 
		 
		 
		parameter [0:0]	OPT_REGISTERED = 0,
		
		 
		 
		 
		parameter [0:0]	OPT_LOWPOWER = 0
		 
	) (
		 
		input	wire			i_clk, i_reset,
		
		input	wire			i_valid,
		output	reg			o_stall,
		input	wire	[AW-1:0]	i_addr,
		input	wire	[DW-1:0]	i_data,
		
		output	reg			o_valid,
		input	wire			i_stall,
		output	reg	[NS:0]		o_decode,
		output	reg	[AW-1:0]	o_addr,
		output	reg	[DW-1:0]	o_data
		 
	);

`line 127 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	 
	 
	
	 
	 
	 
	 
	 
	localparam [0:0] OPT_NONESEL = (!ACCESS_ALLOWED[0])
					|| (SLAVE_MASK[AW-1:0] != 0);
	
	wire	[NS:0]		request;
	reg	[NS-1:0]	prerequest;
	integer			iM;
	 

`line 143 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	 
	 
	always @(*)
	for(iM=0; iM<NS; iM=iM+1)
		prerequest[iM] = (((i_addr ^ SLAVE_ADDR[iM*AW +: AW])
				&SLAVE_MASK[iM*AW +: AW])==0)
			&&(ACCESS_ALLOWED[iM]);
	 

`line 152 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	 
	 
	generate if (OPT_NONESEL)
	begin : NO_DEFAULT_REQUEST
		 
		reg	[NS-1:0]	r_request;

`line 159 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
		 
		
		always @(*)
		begin
			for(iM=0; iM<NS; iM=iM+1)
				r_request[iM] = i_valid && prerequest[iM];
			if (!OPT_NONESEL && (NS > 1 && |prerequest[NS-1:1]))
				r_request[0] = 1'b0;
		end

`line 169 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
		assign	request[NS-1:0] = r_request;
		 
	end else if (NS == 1)
	begin : SINGLE_SLAVE
		 
		assign request[0] = i_valid;

`line 176 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
		/*verilator lint_off UNUSED*/
		wire	unused;
		assign	unused = &{ 1'b0, prerequest };
		/*verilator lint_on UNUSED*/
		 
	end else begin : GENERAL_CASE
		 
		reg	[NS-1:0]	r_request;

`line 185 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
		always @(*)
		begin
			for(iM=0; iM<NS; iM=iM+1)
				r_request[iM] = i_valid && prerequest[iM];
			if (!OPT_NONESEL && (NS > 1 && |prerequest[NS-1:1]))
				r_request[0] = 1'b0;
		end

`line 193 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
		assign	request[NS-1:0] = r_request;
		 
	end endgenerate
	 

`line 198 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	 
	 
	generate if (OPT_NONESEL)
	begin : GENERATE_NONSEL_SLAVE
		reg	r_request_NS, r_none_sel;

`line 204 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
		always @(*)
		begin
			 
			 
			
			 
			 
			 
			r_none_sel = i_valid && (prerequest == 0);
			
			 
			 
			 
			
			r_request_NS = r_none_sel;
		end

`line 221 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
		assign request[NS] = r_request_NS;
	end else begin : NO_NONESEL_SLAVE
		assign request[NS] = 1'b0;
	end endgenerate
	 

`line 227 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	 
	 
	generate if (OPT_REGISTERED)
	begin : GEN_REG_OUTPUTS

`line 232 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
		 
		 
		initial	o_valid = 0;
		always @(posedge i_clk)
		if (i_reset)
			o_valid <= 0;
		else if (!o_stall)
			o_valid <= i_valid;
		 

`line 242 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
		 
		 
		initial	o_addr   = 0;
		initial	o_data   = 0;
		always @(posedge i_clk)
		if (i_reset && OPT_LOWPOWER)
		begin
			o_addr   <= 0;
			o_data   <= 0;
		end else if ((!o_valid || !i_stall)
				 && (i_valid || !OPT_LOWPOWER))
		begin
			o_addr   <= i_addr;
			o_data   <= i_data;
		end else if (OPT_LOWPOWER && !i_stall)
		begin
			o_addr   <= 0;
			o_data   <= 0;
		end
		 

`line 263 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
		 
		 
		initial	o_decode = 0;
		always @(posedge i_clk)
		if (i_reset)
			o_decode <= 0;
		else if ((!o_valid || !i_stall)
				 && (i_valid || !OPT_LOWPOWER))
			o_decode <= request;
		else if (OPT_LOWPOWER && !i_stall)
			o_decode <= 0;
		 

`line 276 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
		 
		 
		always @(*)
			o_stall = (o_valid && i_stall);
		 
	end else begin : GEN_COMBINATORIAL_OUTPUTS

`line 283 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
		always @(*)
		begin
			o_valid = i_valid;
			o_stall = i_stall;
			o_addr  = i_addr;
			o_data  = i_data;

`line 290 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
			o_decode = request;
		end

`line 293 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
		 
		 
		/*verilator coverage_off*/
		/*verilator lint_off UNUSED*/
		wire	unused;
		assign	unused = &{ 1'b0,
	
				 
				 
				i_clk,

`line 304 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
				i_reset };
		/*verilator lint_on UNUSED*/
		/*verilator coverage_on*/
		 
	end endgenerate
	 
 
 
 

`line 314 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
 
 
 
 
 
	
		
		  
	  
		  

`line 325 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
			
	 
		     

`line 329 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	
	  
	 
		

`line 334 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	  
	 
		

`line 338 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	
	  
	     
	
		
		  
	       
	
		
		
		
	

`line 351 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	
	
	 
		    

`line 356 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	 
	  
	 
	
		
		    
				   
			 
		
		
		  
	

`line 369 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	 
	  
	 
		

`line 374 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	
	
	    
	
		 
		 
		
			    
			  
			    
		
	 
	

`line 388 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	
	
	
	
	
	 
		

`line 396 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
		
	 
	
		  
		  
		   
			  
	

`line 405 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	 
	   
		

`line 409 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	

`line 411 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	
	
	
	
	
	
	

`line 419 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	
	
	
			

`line 424 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	  
		

`line 427 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	  
		

`line 430 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	  
		  

`line 433 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
		  
	  
	 
		  
	  
		    

`line 440 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	    
			       
	

`line 444 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
		 
			

`line 447 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
		  
		   
			

`line 451 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	  

`line 453 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
		 
			

`line 456 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
		  
		   
			

`line 460 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
	 
	
	 
 
endmodule
	
`default_nettype wire


`line 469 "third_party/wb2axip_candidate/rtl/addrdecode.v" 0
`line 1 "third_party/wb2axip_candidate/rtl/wbxbar.v" 1
 

`line 3 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
 
 
 

`line 7 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
 
 
 

`line 11 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
 
 
 
 
 

`line 17 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
 
 
 
 
 
 

`line 24 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
 

`line 26 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
 

`line 28 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
 
 
 

`line 32 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
 
 
 
 

`line 37 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
 
 
 

`line 41 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
 
 

`line 44 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
 
 
 
 


`line 50 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
 
 

`line 53 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
 
 
 
 
 

`line 59 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
 
 
 
 
 
 
 
 
 
 
 
 

`line 72 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
 

`line 74 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
`default_nettype none
 
module	wbxbar #(
		 
		parameter	NM = 4, NS=8,
		parameter	AW = 32, DW=32,
		parameter	[NS*AW-1:0]	SLAVE_ADDR = {
				{ 3'b111, {(AW-3){1'b0}} },
				{ 3'b110, {(AW-3){1'b0}} },
				{ 3'b101, {(AW-3){1'b0}} },
				{ 3'b100, {(AW-3){1'b0}} },
				{ 3'b011, {(AW-3){1'b0}} },
				{ 3'b010, {(AW-3){1'b0}} },
				{ 4'b0010, {(AW-4){1'b0}} },
				{ 4'b0000, {(AW-4){1'b0}} } },
		parameter	[NS*AW-1:0]	SLAVE_MASK = (NS <= 1) ? 0
			: { {(NS-2){ 3'b111, {(AW-3){1'b0}} }},
				{(2){ 4'b1111, {(AW-4){1'b0}} }} },
		
		 
		 
		 
		 
		parameter	LGMAXBURST=6,
		
		 
		 
		 
		 
		 
		parameter	OPT_TIMEOUT = 0,  
		
		 
		 
		 
		 
		 
		 
		 
		 
		parameter [0:0]	OPT_STARVATION_TIMEOUT = 1'b0
						&& (OPT_TIMEOUT > 0),
		
		 
		 
		 
		parameter [0:0]	OPT_DBLBUFFER = 1'b0,
		
		 
		 
		 
		 
		 
		parameter [0:0]	OPT_LOWPOWER = 1'b1
		 
	) (
		 
		input	wire			i_clk, i_reset,
		
		 
		input	wire	[NM-1:0]	i_mcyc, i_mstb, i_mwe,
		input	wire	[NM*AW-1:0]	i_maddr,
		input	wire	[NM*DW-1:0]	i_mdata,
		input	wire	[NM*DW/8-1:0]	i_msel,
		
		 
		output	wire	[NM-1:0]	o_mstall,
		output	wire	[NM-1:0]	o_mack,
		output	reg	[NM*DW-1:0]	o_mdata,
		output	wire	[NM-1:0]	o_merr,
		
		
		 
		 
		output	wire	[NS-1:0]	o_scyc, o_sstb, o_swe,
		output	wire	[NS*AW-1:0]	o_saddr,
		output	wire	[NS*DW-1:0]	o_sdata,
		output	wire	[NS*DW/8-1:0]	o_ssel,
		
		 
		input	wire	[NS-1:0]	i_sstall, i_sack,
		input	wire	[NS*DW-1:0]	i_sdata,
		input	wire	[NS-1:0]	i_serr
		 
	);
	
	
	 
	
	 
	 
	
	 
	 
	localparam	TIMEOUT_WIDTH = $clog2(OPT_TIMEOUT);
	
	 
	 
	localparam	LGNM = (NM>1) ? $clog2(NM) : 1;
	
	 
	 
	 
	 
	 
	localparam	LGNS = $clog2(NS+1);
	 
	 
	 
	
	 
	 
	
	 
	 
	 
	 
	
	 
	wire	[NS:0]			request		[0:NM-1];
	reg	[NS-1:0]		requested	[0:NM-1];
	wire	[NS:0]			grant		[0:NM-1];
	wire	[NM-1:0]		mgrant;
	wire	[NS-1:0]		sgrant;

`line 199 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	/*verilator lint_off UNUSED*/
	wire	[LGMAXBURST-1:0]	w_mpending [0:NM-1];
	/*verilator lint_on UNUSED*/
	wire	[NM-1:0]		mfull, mnearfull, mempty;
	wire	[NM-1:0]		timed_out;

`line 205 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	localparam	NMFULL = (NM > 1) ? (1<<LGNM) : 1;
	localparam	NSFULL = (1<<LGNS);

`line 208 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	wire	[LGNS-1:0]	mindex		[0:NMFULL-1];
	wire	[LGNM-1:0]	sindex		[0:NSFULL-1];

`line 211 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	wire	[NMFULL-1:0]	m_cyc;
	wire	[NMFULL-1:0]	m_stb;
	wire	[NMFULL-1:0]	m_we;
	wire	[AW-1:0]	m_addr		[0:NMFULL-1];
	wire	[DW-1:0]	m_data		[0:NMFULL-1];
	wire	[DW/8-1:0]	m_sel		[0:NMFULL-1];
	reg	[NM-1:0]	m_stall;
	
	wire	[NSFULL-1:0]	s_stall;
	wire	[DW-1:0]	s_data		[0:NSFULL-1];
	wire	[NSFULL-1:0]	s_ack;
	wire	[NSFULL-1:0]	s_err;
	wire	[NM-1:0]	dcd_stb;

`line 225 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	localparam [0:0]	OPT_BUFFER_DECODER=(NS != 1 || SLAVE_MASK != 0);
	 
	 
	
	 
	 
	 
	
	

`line 235 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	genvar	N, M;
	integer	iN, iM;
	generate for(N=0; N<NM; N=N+1)
	begin : DECODE_REQUEST
		 
		 
		 
		wire			skd_stb, skd_stall;
		wire			skd_we;
		wire	[AW-1:0]	skd_addr;
		wire	[DW-1:0]	skd_data;
		wire	[DW/8-1:0]	skd_sel;
		wire	[NS:0]		decoded;
		wire			iskd_ready;
		 

`line 251 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		skidbuffer #(
			 
			 
			 
			
			 
			.DW(1+AW+DW+DW/8),
	
			

`line 261 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			.OPT_OUTREG(0)
			 
		) iskid (
			 
			.i_clk(i_clk),
			.i_reset(i_reset || !i_mcyc[N]),
			.i_valid(i_mstb[N]), .o_ready(iskd_ready),
			.i_data({ i_mwe[N], i_maddr[N*AW +: AW],
					i_mdata[N*DW +: DW],
					i_msel[N*DW/8 +: DW/8] }),
			.o_valid(skd_stb), .i_ready(!skd_stall),
				.o_data({ skd_we, skd_addr, skd_data, skd_sel })
			 
		);

`line 276 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		assign	o_mstall[N] = !iskd_ready;

`line 278 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		addrdecode #(
			 
			 
			 
			
			 
			.NS(NS), .AW(AW), .DW(DW+DW/8+1),
			.SLAVE_ADDR(SLAVE_ADDR),
			.SLAVE_MASK(SLAVE_MASK),
			.OPT_REGISTERED(OPT_BUFFER_DECODER)
			 
		) adcd(
			 
			.i_clk(i_clk), .i_reset(i_reset),
			.i_valid(skd_stb && i_mcyc[N]), .o_stall(skd_stall),
				.i_addr(skd_addr),
				.i_data({ skd_we, skd_data, skd_sel }),
			.o_valid(dcd_stb[N]), .i_stall(m_stall[N]&&i_mcyc[N]),
			.o_decode(decoded), .o_addr(m_addr[N]),
				.o_data({ m_we[N], m_data[N], m_sel[N] })
			 
		);

`line 301 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		assign	request[N] = (m_cyc[N] && dcd_stb[N]) ? decoded : 0;

`line 303 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		assign	m_cyc[N] = i_mcyc[N];
		assign	m_stb[N] = i_mcyc[N] && dcd_stb[N] && !mfull[N];
		 
	end for(N=NM; N<NMFULL; N=N+1)
	begin : UNUSED_MASTER_SIGNALS
		 
		 
		 
		assign	m_cyc[N] = 0;
		assign	m_stb[N] = 0;

`line 314 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		assign	m_we[N]   = 0;
		assign	m_addr[N] = 0;
		assign	m_data[N] = 0;
		assign	m_sel[N]  = 0;
		 
	end endgenerate

`line 321 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	 
	 
	always @(*)
	begin
		for(iM=0; iM<NS; iM=iM+1)
		begin
			 
			requested[0][iM] = 0;
			for(iN=1; iN<NM; iN=iN+1)
			begin
				 
				 
				
				 
				requested[iN][iM] = requested[iN-1][iM];
				
				 
				 
				 
				if (request[iN-1][iM] &&
					(grant[iN-1][iM]
					|| (!mgrant[iN-1]||mempty[iN-1])))
					requested[iN][iM] = 1;
			end
		end
	end
	 

`line 349 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	generate for(M=0; M<NS; M=M+1)
	begin : SLAVE_GRANT
		 
	
	
		 
		reg	drop_sgrant;

`line 357 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		 
		always @(*)
		begin
			drop_sgrant = !m_cyc[sindex[M]];
			if (!request[sindex[M]][M] && m_stb[sindex[M]]
				&& mempty[sindex[M]])
				drop_sgrant = 1;
			if (!sgrant[M])
				drop_sgrant = 0;
			if (i_reset)
				drop_sgrant = 1;
		end
		 

`line 372 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		 
		reg	r_sgrant;

`line 376 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		initial	r_sgrant = 0;
		always @(posedge i_clk)
		begin
			r_sgrant <= sgrant[M];
			for(iN=0; iN<NM; iN=iN+1)
			if (request[iN][M] && (!mgrant[iN] || mempty[iN]))
				r_sgrant <= 1;
			if (drop_sgrant)
				r_sgrant <= 0;
		end

`line 387 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		assign	sgrant[M] = r_sgrant;
		 
		 

`line 391 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		
		
		
			

`line 396 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		
			  
			  
			 
				  
		

`line 404 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			  
		
		


`line 409 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		assign	s_data[M]  = i_sdata[M*DW +: DW];
		assign	s_stall[M] = o_sstb[M] && i_sstall[M];
		assign	s_ack[M]   = o_scyc[M] && i_sack[M];
		assign	s_err[M]   = o_scyc[M] && i_serr[M];

`line 414 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
	end for(M=NS; M<NSFULL; M=M+1)
	begin : UNUSED_SLAVE_SIGNALS
		 
		assign	s_data[M]  = 0;
		assign	s_stall[M] = 1;
		assign	s_ack[M]   = 0;
		assign	s_err[M]   = 1;
		 
	end endgenerate

`line 425 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	
	 
	 
	generate for(N=0; N<NM; N=N+1)
	begin : ARBITRATE_REQUESTS
		 

`line 432 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		 
		wire	[NS:0]		regrant;
		wire	[LGNS-1:0]	reindex;

`line 437 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		
		 
		 
		 
		 
		
		 
		 
		 
		 
		 
		
		 
		 
		 
		
		 
		 
		 
		
		 
		 
		 
		
		 
		 
		 
		 
		
		 
		 
		 
		 
		
		reg	stay_on_channel;
		reg	requested_channel_is_available;
		 

`line 476 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		 
		always @(*)
		begin
			stay_on_channel = |(request[N] & grant[N]);

`line 482 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			if (mgrant[N] && !mempty[N])
				stay_on_channel = 1;
		end
		 

`line 487 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		 
		always @(*)
		begin
			requested_channel_is_available =
			|(request[N][NS-1:0]& ~sgrant & ~requested[N][NS-1:0]);

`line 494 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			if (request[N][NS])
				requested_channel_is_available = 1;

`line 497 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			if (NM < 2)
				requested_channel_is_available = m_stb[N];
		end
		 

`line 502 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		 
		reg		r_mgrant;
		reg	[NS:0]	r_grant;

`line 507 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		initial	r_grant = 0;
		initial	r_mgrant = 0;
		always @(posedge i_clk)
		if (i_reset || !i_mcyc[N])
		begin
			r_grant  <= 0;
			r_mgrant <= 0;
		end else if (!stay_on_channel)
		begin
			if (requested_channel_is_available)
			begin
				r_mgrant <= 1'b1;
				r_grant  <= request[N];
			end else if (m_stb[N])
			begin
				r_mgrant <= 1'b0;
				r_grant  <= 0;
			end
		end

`line 527 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		assign	mgrant[N] = r_mgrant;
		assign	grant[N]  = r_grant;
		 

`line 531 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		if (NS == 1)
		begin : MINDEX_ONE_SLAVE
			 
			assign	mindex[N] = 0;
			assign	regrant = 0;
			assign	reindex = 0;

`line 538 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			/*verilator lint_off UNUSED*/
			wire	unused_regrant = &{ 1'b0, regrant, reindex };
			 
			 
		end else begin : MINDEX_MULTIPLE_SLAVES
			 
			reg	[LGNS-1:0]	r_mindex;

`line 546 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	
	
			 
			reg	[NS:0]		r_regrant;
			reg	[LGNS-1:0]	r_reindex;

`line 552 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			 
			 
			always @(*)
			begin
				r_regrant = 0;
				for(iM=0; iM<NS; iM=iM+1)
				begin
					if (grant[N][iM])
						 
						r_regrant[iM] = 1'b1;
					else if (!sgrant[iM]&&!requested[N][iM])
						r_regrant[iM] = 1'b1;

`line 565 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
					if (!request[N][iM])
						r_regrant[iM] = 1'b0;
				end

`line 569 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
				if (grant[N][NS])
					r_regrant[NS] = 1;
				if (!request[N][NS])
					r_regrant[NS] = 0;

`line 574 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
				if (mgrant[N] && !mempty[N])
					r_regrant = 0;
			end
			 

`line 579 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			 
			 
			/*verilator lint_off BLKSEQ*/
			always @(r_regrant, regrant)
			begin
				r_reindex = 0;
				for(iM=0; iM<=NS; iM=iM+1)
				if (r_regrant[iM])
					r_reindex = r_reindex | iM[LGNS-1:0];
				if (regrant == 0)
					r_reindex = r_mindex;
			end
			/*verilator lint_on BLKSEQ*/
			 

`line 594 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			always @(posedge i_clk)
				r_mindex <= reindex;

`line 597 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			assign	reindex = r_reindex;
			assign	regrant = r_regrant;
			 

`line 601 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			
			  
			   
			

`line 606 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
				  
				
					   
					
						
						  
					   
							 
							 
					
						
						
						  
					
				
			

`line 623 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			
  
			assign	mindex[N] = r_mindex;
			 
		end
		 
	end for (N=NM; N<NMFULL; N=N+1)
	begin : UNUSED_MINDEXES
		 
		assign	mindex[N] = 0;
		 
	end endgenerate

`line 636 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	 
	 
	 
	 
	generate for(M=0; M<NS; M=M+1)
	begin : GEN_SINDEX
		 
		if (NM <= 1)
		begin : SINDEX_SINGLE_MASTER
			 
			 
			 
			assign	sindex[M] = 0;
			 
		end else begin : SINDEX_MORE_THAN_ONE_MASTER
			 
			reg	[LGNM-1:0]	r_sindex;
	
	
			 
			reg	[NM-1:0]	regrant;
			reg	[LGNM-1:0]	reindex;

`line 659 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			always @(*)
			begin
				regrant = 0;
				for (iN=0; iN<NM; iN=iN+1)
				begin
					 
					 
					if (grant[iN][M])
						regrant[iN] = 1;
					else if (!sgrant[M]&& !requested[iN][M])
						regrant[iN] = 1;

`line 671 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
					if (!request[iN][M])
						regrant[iN] = 0;
					if (mgrant[iN] && !mempty[iN])
						regrant[iN] = 0;
				end
			end

`line 678 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			always @(*)
			begin
				reindex = 0;
				 
				 
				 
				if (regrant == 0)
					reindex = sindex[M];
				else for(iN=0; iN<NM; iN=iN+1)
					if (regrant[iN])
						reindex = reindex | iN[LGNM-1:0];
			end

`line 691 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			always @(posedge i_clk)
				r_sindex <= reindex;

`line 694 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			assign	sindex[M] = r_sindex;
			 

`line 697 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			
			  
			   
			
				   
				
					   
						  
					    
							 
						  
				
			

`line 711 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
				  
			

`line 714 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			 
		end
		 
	end for(M=NS; M<NSFULL; M=M+1)
	begin : UNUSED_SINDEXES
		 
		 
		
		 
		 

`line 725 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		assign	sindex[M] = 0;
		 
	end endgenerate
	 
	 
	
	 
	 
	 
	
	

`line 737 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	
	 
	
	 
	generate for(M=0; M<NS; M=M+1)
	begin : GEN_CYC_STB
		 
		reg	r_scyc, r_sstb;

`line 746 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		initial	r_scyc = 0;
		initial	r_sstb = 0;
		always @(posedge i_clk)
		begin
			if (sgrant[M])
			begin

`line 753 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
				if (!i_mcyc[sindex[M]])
				begin
					r_scyc <= 1'b0;
					r_sstb <= 1'b0;
				end else begin
					r_scyc <= 1'b1;

`line 760 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
					if (!r_sstb || !s_stall[M])
						r_sstb <=request[sindex[M]][M]
						  && !mfull[sindex[M]];
				end
			end else begin
				r_scyc  <= 1'b0;
				r_sstb  <= 1'b0;
			end

`line 769 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			if (i_reset || s_err[M])
			begin
				r_scyc <= 1'b0;
				r_sstb <= 1'b0;
			end
		end

`line 776 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		assign	o_scyc[M] = r_scyc;
		assign	o_sstb[M] = r_sstb;
		 
	end endgenerate

`line 781 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	
	 
	
	 
	 
	generate if ((NM == 1) && (!OPT_LOWPOWER))
	begin : ONE_MASTER
		 
		reg			r_swe;
		reg	[AW-1:0]	r_saddr;
		reg	[DW-1:0]	r_sdata;
		reg	[DW/8-1:0]	r_ssel;

`line 794 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		
		 
		 
		
		 
		 
		 
		
		always @(posedge i_clk)
		begin
			r_swe   <= o_swe[0];
			r_saddr <= o_saddr[0+:AW];
			r_sdata <= o_sdata[0+:DW];
			r_ssel  <= o_ssel[0+:DW/8];

`line 809 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			/*verilator lint_off WIDTH*/
			if (sgrant[mindex[0]] && !s_stall[mindex[0]])
			/*verilator lint_on WIDTH*/
			begin
				r_swe   <= m_we[0];
				r_saddr <= m_addr[0];
				r_sdata <= m_data[0];
				r_ssel  <= m_sel[0];
			end
		end

`line 820 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		
		 
		 
		 
		 
		for(M=0; M<NS; M=M+1)
		begin : FOREACH_SLAVE_PORT
			assign	o_swe[M] = r_swe;
			assign	o_saddr[M*AW +: AW] = r_saddr;
			assign	o_sdata[M*DW +: DW] = r_sdata;
			assign	o_ssel[M*DW/8+:DW/8]= r_ssel;
		end

`line 833 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
	end else begin : J
	for(M=0; M<NS; M=M+1)
	begin : GEN_DOWNSTREAM
		 
		reg			r_swe;
		reg	[AW-1:0]	r_saddr;
		reg	[DW-1:0]	r_sdata;
		reg	[DW/8-1:0]	r_ssel;

`line 843 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		always @(posedge i_clk)
		if (OPT_LOWPOWER && !sgrant[M])
		begin
			r_swe   <= 1'b0;
			r_saddr <= 0;
			r_sdata <= 0;
			r_ssel  <= 0;
		end else if (!s_stall[M]) begin
			r_swe   <= m_we[sindex[M]];
			r_saddr <= m_addr[sindex[M]];
			if (OPT_LOWPOWER && !m_we[sindex[M]])
				r_sdata <= 0;
			else
				r_sdata <= m_data[sindex[M]];
			r_ssel<= m_sel[sindex[M]];
		end

`line 860 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		assign	o_swe[M] = r_swe;
		assign	o_saddr[M*AW   +: AW] = r_saddr;
		assign	o_sdata[M*DW   +: DW] = r_sdata;
		assign	o_ssel[M*(DW/8)+:DW/8]= r_ssel;
		 
	end end endgenerate
	 
	 
	
	 
	 
	 
	
	
	generate if (OPT_DBLBUFFER)
	begin : DOUBLE_BUFFERRED_STALL
		 
		for(N=0; N<NM; N=N+1)
		begin : FOREACH_MASTER_PORT
			 
			 
			 
			reg	r_mack, r_merr;

`line 884 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			always @(*)
			begin
				if (grant[N][NS])
					m_stall[N] = 1;
				else if (mgrant[N] && request[N][mindex[N]])
					m_stall[N] = mfull[N] || s_stall[mindex[N]];
				else
					m_stall[N] = m_stb[N];

`line 893 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
				if (o_merr[N])
					m_stall[N] = 0;
			end

`line 897 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			initial	r_mack   = 0;
			initial	r_merr   = 0;
			always @(posedge i_clk)
			begin
				/*verilator lint_off WIDTH*/
				iM = mindex[N];
				/*verilator lint_on WIDTH*/
				r_mack   <= mgrant[N] && s_ack[mindex[N]];
				r_merr   <= mgrant[N] && s_err[mindex[N]];
				if (OPT_LOWPOWER && !mgrant[N])
					o_mdata[N*DW +: DW] <= 0;
				else
					o_mdata[N*DW +: DW] <= s_data[mindex[N]];

`line 911 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
				if (grant[N][NS]||(timed_out[N] && !o_mack[N]))
				begin
					r_mack   <= 1'b0;
					r_merr   <= !o_merr[N];
				end

`line 917 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
				if (i_reset || !i_mcyc[N] || o_merr[N])
				begin
					r_mack   <= 1'b0;
					r_merr   <= 1'b0;
				end
			end

`line 924 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			assign	o_mack[N] = r_mack;

`line 926 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			assign	o_merr[N] = (!OPT_STARVATION_TIMEOUT || i_mcyc[N]) && r_merr;

`line 928 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		end
		 
	end else if (NS == 1)  
	begin : SINGLE_SLAVE
		 
		for(N=0; N<NM; N=N+1)
		begin : FOREACH_MASTER_PORT
			reg	r_mack, r_merr;

`line 937 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			always @(*)
			begin
				m_stall[N] = !mgrant[N] || s_stall[0]
					|| (m_stb[N] && !request[N][0]);
				r_mack     =  mgrant[N] && i_sack[0];
				r_merr     =  mgrant[N] && i_serr[0];
				o_mdata[N*DW +: DW]  = (!mgrant[N] && OPT_LOWPOWER)
					? 0 : i_sdata;

`line 946 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
				if (mfull[N])
					m_stall[N] = 1'b1;

`line 949 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
				if (timed_out[N] && !r_mack)
				begin
					m_stall[N] = 1'b0;
					r_mack     = 1'b0;
					r_merr     = 1'b1;
				end

`line 956 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
				if (grant[N][NS] && m_stb[N])
				begin
					m_stall[N] = 1'b0;
					r_mack     = 1'b0;
					r_merr     = 1'b1;
				end

`line 963 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
				if (!m_cyc[N])
				begin
					r_mack = 1'b0;
					r_merr = 1'b0;
				end
			end

`line 970 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			assign	o_mack[N] = r_mack;
			assign	o_merr[N] = r_merr;
		end
		 
	end else begin : SINGLE_BUFFER_STALL
		 
		for(N=0; N<NM; N=N+1)
		begin : FOREACH_MASTER_PORT
			 
			 
			reg	r_mack, r_merr;

`line 982 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			always @(*)
			begin
				m_stall[N] = 1;
				r_mack     = mgrant[N] && s_ack[mindex[N]];
				r_merr     = mgrant[N] && s_err[mindex[N]];
				if (OPT_LOWPOWER && !mgrant[N])
					o_mdata[N*DW +: DW] = 0;
				else
					o_mdata[N*DW +: DW] = s_data[mindex[N]];

`line 992 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
				if (mgrant[N])
					 
					m_stall[N] = s_stall[mindex[N]]
					    || !request[N][mindex[N]];

`line 997 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
				if (mfull[N])
					m_stall[N] = 1'b1;

`line 1000 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
				if (grant[N][NS] ||(timed_out[N] && !r_mack))
				begin
					m_stall[N] = 1'b0;
					r_mack     = 1'b0;
					r_merr     = 1'b1;
				end

`line 1007 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
				if (!m_cyc[N])
				begin
					r_mack    = 1'b0;
					r_merr     = 1'b0;
				end
			end

`line 1014 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			assign	o_mack[N] = r_mack;
			assign	o_merr[N] = r_merr;
		end
		 
	end endgenerate

`line 1020 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	
	 
	generate for(N=0; N<NM; N=N+1)
	begin : COUNT_PENDING_TRANSACTIONS
		 
		reg	[LGMAXBURST-1:0]	lclpending;
		reg				r_empty, r_nearfull, r_full;

`line 1028 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		initial	lclpending  = 0;
		initial	r_empty    = 1;
		initial	r_nearfull = 0;
		initial	r_full     = 0;
		always @(posedge i_clk)
		if (i_reset || !i_mcyc[N] || o_merr[N])
		begin
			lclpending <= 0;
			r_full    <= 0;
			r_empty   <= 1'b1;
			r_nearfull<= 0;
		end else case({ (m_stb[N] && !m_stall[N]), o_mack[N] })
		2'b01: begin
			lclpending <= lclpending - 1'b1;
			r_nearfull<= mfull[N];
			r_full    <= 1'b0;
			r_empty   <= (lclpending == 1);
			end
		2'b10: begin
			lclpending <= lclpending + 1'b1;
			r_nearfull<= (&lclpending[LGMAXBURST-1:2])&&(lclpending[1:0] != 0);
			r_full    <= mnearfull[N];
			r_empty   <= 1'b0;
			end
		default: begin end
		endcase

`line 1055 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		assign w_mpending[N]= lclpending;
		assign mempty[N]    = r_empty;
		assign mfull[N]     = r_full;
		assign mnearfull[N] = r_nearfull;
		 
	end endgenerate

`line 1062 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	generate if (OPT_TIMEOUT > 0)
	begin : CHECK_TIMEOUT
		 
		for(N=0; N<NM; N=N+1)
		begin : FOREACH_MASTER_PORT

`line 1068 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			reg	[TIMEOUT_WIDTH-1:0]	deadlock_timer;
			reg				r_timed_out;

`line 1071 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			initial	deadlock_timer = OPT_TIMEOUT;
			initial	r_timed_out = 0;
			always @(posedge i_clk)
			if (i_reset || !i_mcyc[N]
					||((w_mpending[N] == 0) && !m_stb[N])
					||(m_stb[N] && !m_stall[N])
					||(o_mack[N] || o_merr[N])
					||(!OPT_STARVATION_TIMEOUT&&!mgrant[N]))
			begin
				deadlock_timer <= OPT_TIMEOUT;
				r_timed_out <= 0;
			end else if (deadlock_timer > 0)
			begin
				deadlock_timer <= deadlock_timer - 1;
				r_timed_out <= (deadlock_timer <= 1);
			end

`line 1088 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			assign	timed_out[N] = r_timed_out;
		end
		 
	end else begin : NO_TIMEOUT
		 
		assign	timed_out = 0;
		 
	end endgenerate
	 
	 
	
	 
	 
	 
	
	
	initial	begin : PARAMETER_CONSISTENCY_CHECK
		 
		if (NM == 0)
		begin
			$display("ERROR: At least one master must be defined");
			$stop;
		end

`line 1112 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		if (NS == 0)
		begin
			$display("ERROR: At least one slave must be defined");
			$stop;
		end

`line 1118 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		if (OPT_STARVATION_TIMEOUT != 0 && OPT_TIMEOUT == 0)
		begin
			$display("ERROR: The starvation timeout is implemented as part of the regular timeout");
			$display("  Without a timeout, the starvation timeout will not work");
			$stop;
		end
		 
	end
	 
 
 
 

`line 1131 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
 
 
 
 
 
	
	
	
		  
		  
	
				
	
	
	
	
					
					
				
	
	
					
					
				
	

`line 1157 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		    

`line 1159 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		  
	  
		  

`line 1163 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	 
	 
		

`line 1167 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	   
	  
		
			

`line 1172 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		 
		  
			
			
			
			  

`line 1180 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		  
		
			
			 
			   
				  
		


`line 1189 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		 
			  

`line 1193 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		 
		
			  
			  
				 
					  
			 
				  

`line 1203 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			  
		
		
	 

`line 1208 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	
	   
	  
		
		  
		
			 
			 
			
				
				  
				
				  
			
		
		
	 

`line 1226 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	   
	  
		
			

`line 1231 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		 
			

`line 1235 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		
			  
			  
			 
				  
		

`line 1243 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
			  
		
	 

`line 1248 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	
	   
	  
		
		 
		 
		
			    
			
			  
		
		
	 

`line 1262 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	
	
	
	
	
	 
	 
		  

`line 1271 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	   
	
		 
		 
		
			  
			  
			  
		
	 

`line 1282 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	   
	
		 
		 
		
			  
			  
		
	 
	


`line 1294 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	
	
	
	
	
	
	
	
	
	
	   
	  
		
		 
			 
			
			
			
			  
				  
				     
				  
			     
			  

`line 1319 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		 
			  

`line 1323 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		     
			  

`line 1327 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		  
		       
			  
		
	 

`line 1333 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	   
	  
		
		 
			 
			
			
			
			  
				  
				     
				  
			   
			  
		
	 
	
	
	
	
	
	
	
	
	   
	  
		
		 
		 
			

`line 1364 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		  
		 
			  
				    

`line 1369 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
				
		 
		 
			 
				    
				     

`line 1376 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
			  
				     
				     

`line 1381 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		  
		     
			
				     

`line 1386 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		      
		  
		       
			
				 
					  

`line 1393 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		 
		
			  
			   
			
				   
					  
				 
					  
				 
					  
				   
					  
				   
					  
				   
					  
			
		

`line 1414 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		     
		
			 
				  
		
		
	 

`line 1423 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	   
	  
		
		  
		 
			
		
	 
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	   		
					
	   		
					

`line 1471 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	 
	   
		  
	 
	   
		  

`line 1478 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	
	
	 
	
		  
		    
		
			     
					    
				  
		
	

`line 1491 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	    
	  
		
		
		
		
		
			

`line 1500 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		 
		
			  
			    
			
				     
						    
				
					  
					  
				
			
		
		
	 
	
	
	
	
	
	
	
	
	
	
	 
	 
		  

`line 1530 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		  

`line 1532 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	  
	   
	
		
		   
		
			

`line 1540 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			 
					    
				 
						 
		 
			
		

`line 1548 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
			
				 

`line 1552 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		   
			 
		
			    
			     
				          
		
		
	

`line 1562 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	
	
	
	
			
			 

`line 1569 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		  
	  
		  

`line 1573 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	 
		    
					 
		  
	  
	     
			
			
	
		  
		 
			
			  
			
			
		
			  
		

`line 1592 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		
			
			
			
			  
			  
			
		

`line 1602 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		   
		
			
			
			
			    

`line 1609 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			  

`line 1611 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		     
		
			
			
			  

`line 1617 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			  
		

`line 1620 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		   
		
			
			
			
			    
			  
		     
		
			
			    
			 
				  
		

`line 1635 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		
			
			    
				 
		
	 
		  

`line 1644 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	 
		  

`line 1647 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	
	
	
	
			
			 

`line 1654 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		  
	  
		  

`line 1658 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	 
		  
				 
					 
		  
	  
	     
			
			
	
		  
		 
			
			  
			
		
			
			
			
			  
		

`line 1680 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		 
		
			
			
			
			  
			  
			
		

`line 1690 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		   
		
			
			
			
			    
			  
				 
			  
				 

`line 1701 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			  

`line 1703 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		     
		
			
			
			  
			
			

`line 1711 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			  
		

`line 1714 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		   
		
			
			
			
			    
			  
			  
			  
		     
		
			  
			
				     
					  
						   
			

`line 1732 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
			
			 
				  
		

`line 1737 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		     
					 
			
	 
		  

`line 1743 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	 
		  
	
	
	
	
	
	
	
	
			
			
				

`line 1757 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		  
	  
	   
		  
	   
	
		 
			  
		 
		
			   
				  
		
	

`line 1772 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		  
	    
	  

`line 1776 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		  
		 
			  
		  
			  

`line 1782 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	 

`line 1784 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	  
		  

`line 1787 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	    
	

`line 1790 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		  
			  

`line 1793 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	 

`line 1795 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		  
	    
	  

`line 1799 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		  
		 
			  
		    
			  

`line 1805 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	 

`line 1807 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	  
		  

`line 1810 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	    
	

`line 1813 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
		  
			  

`line 1816 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
	 
	

`line 1819 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
 
endmodule
	
`default_nettype wire


`line 1825 "third_party/wb2axip_candidate/rtl/wbxbar.v" 0
