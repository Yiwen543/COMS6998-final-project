# ROLE: Advanced RTL Verification Engineer & SystemVerilog Agent (E-Graph Augmented)
You are an expert hardware verification engineer specialized in SystemVerilog.
Use supplied semantic evidence to avoid redundant stimulus and maximize DUT line,
branch, and toggle coverage within the given execution and cycle budgets.

## Inputs
[SPECIFICATION]: Behavioral contract, interfaces, reset polarity/timing, parameters.
[RTL_CODE]: Complete DUT and required submodules/packages. Keep these files fixed.
[E_GRAPH_REPRESENTATION]: Optional normalized predicates, E-classes and E-nodes,
source mappings, bit widths, enclosing guards, and clock/reset context.
An E-class groups proven equivalent expressions. Distinct winners/states are
behavioral partitions and must not be called equivalent. Membership alone does
not prove that every corresponding source location has executed.

## Verification plan
Output a concise, auditable <verification_plan> with four parts:
1. Semantic evidence: identify relevant normalized predicates, dependency guards,
   and temporal context. If extraction is missing/incomplete, state the structural
   assumptions and unsupported semantics explicitly.
2. Corner cases: map concrete cases to predicates, including idle, competing
   requests, override without requests, multi-bit override, reset during an active
   grant, and recovery where relevant.
3. Stimulus: describe directed/constrained-random inputs, drive/sample timing,
   execution/cycle budgets, and the expected coverage targets. Claim measured
   coverage only after simulation; explain unreachable points separately.
4. Checkers: use an independent specification-based oracle and timing checks;
   record DUT defects separately from compilation/checker failures. Do not weaken
   a checker or alter the DUT to make a run pass.
Provide design conclusions and concise rationale, rather than private internal
reasoning. Report assumptions and objective evidence.

## Output
Immediately after </verification_plan>, provide one systemverilog fenced block
containing only a complete, module-based, standalone self-checking testbench.
Include clock, synchronized stimulus/reset, checks after NBA updates, watchdog,
summary, and nonzero failure termination. Avoid proprietary/UVM dependencies.
No file-based stimulus is required for standalone operation.

## Experiment constraints
Record simulator executions AND simulated cycles. Keep model, initial context,
seed, checker contract, token/cycle/execution budgets fixed across configurations:
A logs/checker status; B A + raw source coverage; C B + E-graph semantic feedback.
For research runs record actual API input/output token usage; unavailable is null.
Token ROI = newly hit DUT branch points / (total API tokens / 1000).
Do not treat this hand-authored integration test as evidence of model performance.

[SPECIFICATION]
# Fixed Priority Arbiter Specification Document

## Introduction

The **Fixed Priority Arbiter** is designed to handle **arbitration among multiple requesters** using a **fixed-priority scheme**. It ensures that **only one request** is granted at a time, following a **fixed priority order** (lowest index has the highest priority).  

Additionally, the arbiter **supports external priority overrides**, allowing dynamic control of the granted request. The module operates synchronously with **one-cycle arbitration latency** and provides **valid and grant index outputs** to indicate which request was granted.

---

## Arbitration Overview

The **fixed-priority arbitration** logic follows these steps:

1. **Check Priority Override:**  
   - If `priority_override` is **non-zero**, it takes precedence over the `req` input.
   - The **highest-priority bit** in `priority_override` is granted.

2. **Fixed Priority Selection:**  
   - If `priority_override` is **zero**, the arbiter **scans `req` from bit 0 to 7**.
   - The **first active request** (lowest index) is granted.

3. **Grant Output:**  
   - The grant signal (`grant`) has a **single bit set** corresponding to the granted request.
   - The `grant_index` output provides the **binary index** of the granted request.
   - The `valid` signal is set **high** if a request is granted.

4. **Reset Behavior:**  
   - When `reset` is asserted, the arbiter **clears all outputs** (`grant`, `grant_index`, `valid`).

---

## Module Interface

The module should be defined as follows:

```verilog
module fixed_priority_arbiter(
    input clk,                     
    input reset,                    
    input [7:0] req,                
    input [7:0] priority_override,  

    output reg [7:0] grant,        
    output reg valid,              
    output reg [2:0] grant_index    
);
```

## Port Description
| **Signal**          | **Direction** | **Description**                                                |
|---------------------|---------------|----------------------------------------------------------------|
| `clk`               | **Input**     | System clock (all operations occur on the rising edge).        |
| `reset`             | **Input**     | Active-high synchronous reset (clears all outputs).            |
| `req`               | **Input**     | 8-bit request signal. Each bit represents a requester.         |
| `priority_override` | **Input**     | Allows external modules to force a specific grant.             |
| `grant`             | **Output**    | 8-bit grant signal; only **one bit** is set based on priority. |
| `valid`             | **Output**    | High (`1`) when a grant is issued.                             |
| `grant_index`       | **Output**    | 3-bit index of the granted request.                            |

---

## Internal Architecture

The **Fixed Priority Arbiter** consists of the following components:

### **1. Priority Override Logic**
- Checks if `priority_override` is **non-zero**.
- If so, grants the **highest-priority bit** in `priority_override`.

### **2. Fixed Priority Selection Logic**
- If `priority_override` is **zero**, the arbiter **scans `req` from bit 0 to bit 7**.
- The **lowest active bit** is granted.

### **3. Grant Signal Generation**
- Generates an **8-bit grant signal** with **a single active bit**.
- The corresponding **binary index** is assigned to `grant_index`.

### **4. Output Registering**
- Ensures that **outputs are stable** until the next clock cycle.
- `valid` is set high (`1`) if a request is granted.

---

## Timing and Latency

The **fixed-priority arbitration** is a **single-cycle operation**, meaning that:
| **Operation**           | **Latency (Clock Cycles)** |
|-------------------------|----------------------------|
| **Request Arbitration** | 1 clock cycle              |
| **Priority Override**   | 1 clock cycle              |
| **Reset**               | 1 clock cycle              |

This ensures **fast response times** for **high-speed applications**.

---


[RTL_CODE]
```systemverilog
`timescale 1ns / 1ps
module fixed_priority_arbiter(
    input clk,                      // Clock signal
    input reset,                    // Active high reset signal
    input [7:0] req,                // 8-bit request signal; each bit represents a request from a different source
    input [7:0] priority_override,  // External priority override signal

    output reg [7:0] grant,         // 8-bit grant signal; only one bit will be set high based on priority
    output reg valid,               // Indicates if a request is granted
    output reg [2:0] grant_index    // Outputs the granted request index in binary format
); 

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            grant <= 8'b00000000;
            valid <= 1'b0;
            grant_index <= 3'b000;
        end 
        else begin
            if (priority_override != 8'b00000000) begin
                grant <= priority_override; 
                valid <= 1'b1;
                grant_index <= (priority_override[0] ? 3'd0 :
                                priority_override[1] ? 3'd1 :
                                priority_override[2] ? 3'd2 :
                                priority_override[3] ? 3'd3 :
                                priority_override[4] ? 3'd4 :
                                priority_override[5] ? 3'd5 :
                                priority_override[6] ? 3'd6 :
                                priority_override[7] ? 3'd7 : 3'd0);
            end
            else if (req[0]) begin
                grant <= 8'b00000001;
                grant_index <= 3'd0;
                valid <= 1'b1;
            end 
            else if (req[1]) begin
                grant <= 8'b00000010;
                grant_index <= 3'd1;
                valid <= 1'b1;
            end 
            else if (req[2]) begin
                grant <= 8'b00000100;
                grant_index <= 3'd2;
                valid <= 1'b1;
            end 
            else if (req[3]) begin
                grant <= 8'b00001000;
                grant_index <= 3'd3;
                valid <= 1'b1;
            end 
            else if (req[4]) begin
                grant <= 8'b00010000;
                grant_index <= 3'd4;
                valid <= 1'b1;
            end 
            else if (req[5]) begin
                grant <= 8'b00100000;
                grant_index <= 3'd5;
                valid <= 1'b1;
            end 
            else if (req[6]) begin
                grant <= 8'b01000000;
                grant_index <= 3'd6;
                valid <= 1'b1;
            end 
            else if (req[7]) begin
                grant <= 8'b10000000;
                grant_index <= 3'd7;
                valid <= 1'b1;
            end 
            else begin
                grant <= 8'b00000000;
                grant_index <= 3'd0;
                valid <= 1'b0;
            end
        end
    end
endmodule
```

[E_GRAPH_REPRESENTATION]
```json
{
  "eclasses": [
    {
      "id": 0,
      "nodes": [
        {
          "children": [],
          "op": "reset"
        }
      ]
    },
    {
      "id": 88,
      "nodes": [
        {
          "children": [
            5,
            87
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 25,
      "nodes": [
        {
          "children": [
            4,
            24
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 176,
      "nodes": [
        {
          "children": [],
          "op": "override7"
        }
      ]
    },
    {
      "id": 50,
      "nodes": [
        {
          "children": [],
          "op": "req5"
        }
      ]
    },
    {
      "id": 138,
      "nodes": [
        {
          "children": [
            120
          ],
          "op": "not"
        }
      ]
    },
    {
      "id": 75,
      "nodes": [
        {
          "children": [
            66
          ],
          "op": "not"
        },
        {
          "children": [
            58,
            74
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 163,
      "nodes": [
        {
          "children": [
            107,
            162
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 100,
      "nodes": [
        {
          "children": [
            4,
            99
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 37,
      "nodes": [
        {
          "children": [],
          "op": "req4"
        }
      ]
    },
    {
      "id": 188,
      "nodes": [
        {
          "children": [
            178
          ],
          "op": "not"
        },
        {
          "children": [
            152,
            187
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 62,
      "nodes": [
        {
          "children": [
            54
          ],
          "op": "not"
        },
        {
          "children": [
            14,
            61
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 87,
      "nodes": [
        {
          "children": [
            13,
            86
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 24,
      "nodes": [
        {
          "children": [
            17,
            23
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 175,
      "nodes": [
        {
          "children": [
            101,
            174
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 112,
      "nodes": [
        {
          "children": [
            102,
            107
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 49,
      "nodes": [
        {
          "children": [
            4,
            48
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 74,
      "nodes": [
        {
          "children": [
            50
          ],
          "op": "not"
        }
      ]
    },
    {
      "id": 162,
      "nodes": [
        {
          "children": [
            111,
            161
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 99,
      "nodes": [
        {
          "children": [
            82,
            98
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 36,
      "nodes": [
        {
          "children": [
            4,
            35
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 187,
      "nodes": [
        {
          "children": [
            177
          ],
          "op": "not"
        },
        {
          "children": [
            168,
            186
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 61,
      "nodes": [
        {
          "children": [
            53
          ],
          "op": "not"
        },
        {
          "children": [
            22,
            60
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 86,
      "nodes": [
        {
          "children": [
            17,
            85
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 23,
      "nodes": [
        {
          "children": [
            18
          ],
          "op": "not"
        },
        {
          "children": [
            14,
            22
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 174,
      "nodes": [
        {
          "children": [
            159,
            173
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 111,
      "nodes": [
        {
          "children": [],
          "op": "override2"
        }
      ]
    },
    {
      "id": 48,
      "nodes": [
        {
          "children": [
            37,
            47
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 10,
      "nodes": [
        {
          "children": [],
          "op": "true"
        },
        {
          "children": [
            231
          ],
          "op": "not"
        }
      ]
    },
    {
      "id": 161,
      "nodes": [
        {
          "children": [
            120,
            160
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 98,
      "nodes": [
        {
          "children": [
            88
          ],
          "op": "not"
        },
        {
          "children": [
            14,
            97
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 35,
      "nodes": [
        {
          "children": [
            26,
            34
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 186,
      "nodes": [
        {
          "children": [
            159
          ],
          "op": "not"
        }
      ]
    },
    {
      "id": 60,
      "nodes": [
        {
          "children": [
            52
          ],
          "op": "not"
        },
        {
          "children": [
            32,
            59
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 148,
      "nodes": [
        {
          "children": [
            102,
            147
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 85,
      "nodes": [
        {
          "children": [
            26,
            84
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 22,
      "nodes": [
        {
          "children": [
            13
          ],
          "op": "not"
        }
      ]
    },
    {
      "id": 173,
      "nodes": [
        {
          "children": [
            164
          ],
          "op": "not"
        },
        {
          "children": [
            108,
            172
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 110,
      "nodes": [
        {
          "children": [
            101,
            109
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 47,
      "nodes": [
        {
          "children": [
            40
          ],
          "op": "not"
        },
        {
          "children": [
            14,
            46
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 9,
      "nodes": [
        {
          "children": [
            4,
            5
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 160,
      "nodes": [
        {
          "children": [
            131,
            144
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 97,
      "nodes": [
        {
          "children": [
            87
          ],
          "op": "not"
        },
        {
          "children": [
            22,
            96
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 34,
      "nodes": [
        {
          "children": [
            28
          ],
          "op": "not"
        },
        {
          "children": [
            14,
            33
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 122,
      "nodes": [
        {
          "children": [
            102,
            121
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 59,
      "nodes": [
        {
          "children": [
            51
          ],
          "op": "not"
        },
        {
          "children": [
            44,
            58
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 147,
      "nodes": [
        {
          "children": [
            107,
            146
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 84,
      "nodes": [
        {
          "children": [
            37,
            83
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 172,
      "nodes": [
        {
          "children": [
            163
          ],
          "op": "not"
        },
        {
          "children": [
            116,
            171
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 109,
      "nodes": [
        {
          "children": [
            107,
            108
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 46,
      "nodes": [
        {
          "children": [
            39
          ],
          "op": "not"
        },
        {
          "children": [
            22,
            45
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 134,
      "nodes": [
        {
          "children": [
            102,
            133
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 159,
      "nodes": [
        {
          "children": [],
          "op": "override6"
        }
      ]
    },
    {
      "id": 96,
      "nodes": [
        {
          "children": [
            86
          ],
          "op": "not"
        },
        {
          "children": [
            32,
            95
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 33,
      "nodes": [
        {
          "children": [
            27
          ],
          "op": "not"
        },
        {
          "children": [
            22,
            32
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 121,
      "nodes": [
        {
          "children": [
            107,
            111
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 58,
      "nodes": [
        {
          "children": [
            37
          ],
          "op": "not"
        }
      ]
    },
    {
      "id": 146,
      "nodes": [
        {
          "children": [
            111,
            145
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 83,
      "nodes": [
        {
          "children": [
            50,
            65
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 171,
      "nodes": [
        {
          "children": [
            162
          ],
          "op": "not"
        },
        {
          "children": [
            126,
            170
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 108,
      "nodes": [
        {
          "children": [
            102
          ],
          "op": "not"
        },
        {
          "children": [
            108,
            231
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 45,
      "nodes": [
        {
          "children": [
            38
          ],
          "op": "not"
        },
        {
          "children": [
            32,
            44
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 133,
      "nodes": [
        {
          "children": [
            107,
            132
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 70,
      "nodes": [
        {
          "children": [
            5,
            69
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 158,
      "nodes": [
        {
          "children": [
            101,
            157
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 95,
      "nodes": [
        {
          "children": [
            85
          ],
          "op": "not"
        },
        {
          "children": [
            44,
            94
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 32,
      "nodes": [
        {
          "children": [
            17
          ],
          "op": "not"
        }
      ]
    },
    {
      "id": 120,
      "nodes": [
        {
          "children": [],
          "op": "override3"
        }
      ]
    },
    {
      "id": 145,
      "nodes": [
        {
          "children": [
            120,
            131
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 82,
      "nodes": [
        {
          "children": [],
          "op": "req7"
        }
      ]
    },
    {
      "id": 170,
      "nodes": [
        {
          "children": [
            161
          ],
          "op": "not"
        },
        {
          "children": [
            138,
            169
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 107,
      "nodes": [
        {
          "children": [],
          "op": "override1"
        }
      ]
    },
    {
      "id": 44,
      "nodes": [
        {
          "children": [
            26
          ],
          "op": "not"
        }
      ]
    },
    {
      "id": 132,
      "nodes": [
        {
          "children": [
            111,
            120
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 69,
      "nodes": [
        {
          "children": [
            13,
            68
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 157,
      "nodes": [
        {
          "children": [
            144,
            156
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 94,
      "nodes": [
        {
          "children": [
            84
          ],
          "op": "not"
        },
        {
          "children": [
            58,
            93
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 182,
      "nodes": [
        {
          "children": [
            102,
            181
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 119,
      "nodes": [
        {
          "children": [
            101,
            118
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 144,
      "nodes": [
        {
          "children": [],
          "op": "override5"
        }
      ]
    },
    {
      "id": 81,
      "nodes": [
        {
          "children": [
            4,
            80
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 18,
      "nodes": [
        {
          "children": [
            5,
            13
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 169,
      "nodes": [
        {
          "children": [
            160
          ],
          "op": "not"
        },
        {
          "children": [
            152,
            168
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 194,
      "nodes": [
        {
          "children": [
            101,
            193
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 131,
      "nodes": [
        {
          "children": [],
          "op": "override4"
        }
      ]
    },
    {
      "id": 68,
      "nodes": [
        {
          "children": [
            17,
            67
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 5,
      "nodes": [
        {
          "children": [
            5,
            10
          ],
          "op": "and"
        },
        {
          "children": [],
          "op": "req0"
        }
      ]
    },
    {
      "id": 156,
      "nodes": [
        {
          "children": [
            148
          ],
          "op": "not"
        },
        {
          "children": [
            108,
            155
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 93,
      "nodes": [
        {
          "children": [
            83
          ],
          "op": "not"
        },
        {
          "children": [
            74,
            92
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 181,
      "nodes": [
        {
          "children": [
            107,
            180
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 118,
      "nodes": [
        {
          "children": [
            111,
            117
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 143,
      "nodes": [
        {
          "children": [
            101,
            142
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 80,
      "nodes": [
        {
          "children": [
            65,
            79
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 231,
      "nodes": [
        {
          "children": [],
          "op": "false"
        },
        {
          "children": [
            10
          ],
          "op": "not"
        }
      ]
    },
    {
      "id": 17,
      "nodes": [
        {
          "children": [],
          "op": "req2"
        }
      ]
    },
    {
      "id": 168,
      "nodes": [
        {
          "children": [
            144
          ],
          "op": "not"
        }
      ]
    },
    {
      "id": 193,
      "nodes": [
        {
          "children": [
            176,
            192
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 130,
      "nodes": [
        {
          "children": [
            101,
            129
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 67,
      "nodes": [
        {
          "children": [
            26,
            66
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 4,
      "nodes": [
        {
          "children": [
            1,
            3
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 155,
      "nodes": [
        {
          "children": [
            147
          ],
          "op": "not"
        },
        {
          "children": [
            116,
            154
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 92,
      "nodes": [
        {
          "children": [
            65
          ],
          "op": "not"
        }
      ]
    },
    {
      "id": 180,
      "nodes": [
        {
          "children": [
            111,
            179
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 117,
      "nodes": [
        {
          "children": [
            112
          ],
          "op": "not"
        },
        {
          "children": [
            108,
            116
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 54,
      "nodes": [
        {
          "children": [
            5,
            53
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 142,
      "nodes": [
        {
          "children": [
            131,
            141
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 79,
      "nodes": [
        {
          "children": [
            70
          ],
          "op": "not"
        },
        {
          "children": [
            14,
            78
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 16,
      "nodes": [
        {
          "children": [
            4,
            15
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 104,
      "nodes": [
        {
          "children": [
            101,
            102
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 192,
      "nodes": [
        {
          "children": [
            182
          ],
          "op": "not"
        },
        {
          "children": [
            108,
            191
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 129,
      "nodes": [
        {
          "children": [
            120,
            128
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 66,
      "nodes": [
        {
          "children": [
            37,
            50
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 3,
      "nodes": [
        {
          "children": [
            2
          ],
          "op": "not"
        }
      ]
    },
    {
      "id": 154,
      "nodes": [
        {
          "children": [
            146
          ],
          "op": "not"
        },
        {
          "children": [
            126,
            153
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 28,
      "nodes": [
        {
          "children": [
            5,
            27
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 179,
      "nodes": [
        {
          "children": [
            120,
            178
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 116,
      "nodes": [
        {
          "children": [
            107
          ],
          "op": "not"
        }
      ]
    },
    {
      "id": 53,
      "nodes": [
        {
          "children": [
            13,
            52
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 141,
      "nodes": [
        {
          "children": [
            134
          ],
          "op": "not"
        },
        {
          "children": [
            108,
            140
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 78,
      "nodes": [
        {
          "children": [
            69
          ],
          "op": "not"
        },
        {
          "children": [
            22,
            77
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 15,
      "nodes": [
        {
          "children": [
            13,
            14
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 40,
      "nodes": [
        {
          "children": [
            5,
            39
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 191,
      "nodes": [
        {
          "children": [
            181
          ],
          "op": "not"
        },
        {
          "children": [
            116,
            190
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 128,
      "nodes": [
        {
          "children": [
            122
          ],
          "op": "not"
        },
        {
          "children": [
            108,
            127
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 65,
      "nodes": [
        {
          "children": [],
          "op": "req6"
        }
      ]
    },
    {
      "id": 2,
      "nodes": [
        {
          "children": [],
          "op": "override_any"
        }
      ]
    },
    {
      "id": 153,
      "nodes": [
        {
          "children": [
            145
          ],
          "op": "not"
        },
        {
          "children": [
            138,
            152
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 27,
      "nodes": [
        {
          "children": [
            13,
            17
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 178,
      "nodes": [
        {
          "children": [
            131,
            177
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 52,
      "nodes": [
        {
          "children": [
            17,
            51
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 140,
      "nodes": [
        {
          "children": [
            133
          ],
          "op": "not"
        },
        {
          "children": [
            116,
            139
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 77,
      "nodes": [
        {
          "children": [
            68
          ],
          "op": "not"
        },
        {
          "children": [
            32,
            76
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 14,
      "nodes": [
        {
          "children": [
            5
          ],
          "op": "not"
        },
        {
          "children": [
            14,
            231
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 102,
      "nodes": [
        {
          "children": [
            102,
            10
          ],
          "op": "and"
        },
        {
          "children": [],
          "op": "override0"
        }
      ]
    },
    {
      "id": 39,
      "nodes": [
        {
          "children": [
            13,
            38
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 190,
      "nodes": [
        {
          "children": [
            180
          ],
          "op": "not"
        },
        {
          "children": [
            126,
            189
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 127,
      "nodes": [
        {
          "children": [
            121
          ],
          "op": "not"
        },
        {
          "children": [
            116,
            126
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 64,
      "nodes": [
        {
          "children": [
            4,
            63
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 1,
      "nodes": [
        {
          "children": [
            0
          ],
          "op": "not"
        }
      ]
    },
    {
      "id": 152,
      "nodes": [
        {
          "children": [
            131
          ],
          "op": "not"
        }
      ]
    },
    {
      "id": 26,
      "nodes": [
        {
          "children": [],
          "op": "req3"
        }
      ]
    },
    {
      "id": 177,
      "nodes": [
        {
          "children": [
            144,
            159
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 51,
      "nodes": [
        {
          "children": [
            26,
            37
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 139,
      "nodes": [
        {
          "children": [
            132
          ],
          "op": "not"
        },
        {
          "children": [
            126,
            138
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 76,
      "nodes": [
        {
          "children": [
            67
          ],
          "op": "not"
        },
        {
          "children": [
            44,
            75
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 13,
      "nodes": [
        {
          "children": [],
          "op": "req1"
        }
      ]
    },
    {
      "id": 164,
      "nodes": [
        {
          "children": [
            102,
            163
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 101,
      "nodes": [
        {
          "children": [
            1,
            2
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 38,
      "nodes": [
        {
          "children": [
            17,
            26
          ],
          "op": "or"
        }
      ]
    },
    {
      "id": 189,
      "nodes": [
        {
          "children": [
            179
          ],
          "op": "not"
        },
        {
          "children": [
            138,
            188
          ],
          "op": "and"
        }
      ]
    },
    {
      "id": 126,
      "nodes": [
        {
          "children": [
            111
          ],
          "op": "not"
        }
      ]
    },
    {
      "id": 63,
      "nodes": [
        {
          "children": [
            50,
            62
          ],
          "op": "and"
        }
      ]
    }
  ],
  "engine": "egg 0.11.0",
  "iterations": 7,
  "semantics": "pure two-state one-bit Boolean predicates",
  "stop_reason": "Some(Saturated)",
  "targets": [
    {
      "eclass": 9,
      "equivalent": true,
      "id": "req_0",
      "representative": "(and (and (not reset) (not override_any)) req0)"
    },
    {
      "eclass": 16,
      "equivalent": true,
      "id": "req_1",
      "representative": "(and (and (not reset) (not override_any)) (and req1 (not req0)))"
    },
    {
      "eclass": 25,
      "equivalent": true,
      "id": "req_2",
      "representative": "(and (and (not reset) (not override_any)) (and req2 (not (or req0 req1))))"
    },
    {
      "eclass": 36,
      "equivalent": true,
      "id": "req_3",
      "representative": "(and (and (not reset) (not override_any)) (and req3 (not (or req0 (or req1 req2)))))"
    },
    {
      "eclass": 49,
      "equivalent": true,
      "id": "req_4",
      "representative": "(and (and (not reset) (not override_any)) (and req4 (not (or req0 (or req1 (or req2 req3))))))"
    },
    {
      "eclass": 64,
      "equivalent": true,
      "id": "req_5",
      "representative": "(and (and (not reset) (not override_any)) (and req5 (not (or req0 (or req1 (or req2 (or req3 req4)))))))"
    },
    {
      "eclass": 81,
      "equivalent": true,
      "id": "req_6",
      "representative": "(and (and (not reset) (not override_any)) (and req6 (not (or req0 (or req1 (or req2 (or req3 (or req4 req5))))))))"
    },
    {
      "eclass": 100,
      "equivalent": true,
      "id": "req_7",
      "representative": "(and (and (not reset) (not override_any)) (and req7 (not (or req0 (or req1 (or req2 (or req3 (or req4 (or req5 req6)))))))))"
    },
    {
      "eclass": 104,
      "equivalent": true,
      "id": "override_0",
      "representative": "(and (and (not reset) override_any) override0)"
    },
    {
      "eclass": 110,
      "equivalent": true,
      "id": "override_1",
      "representative": "(and (and (not reset) override_any) (and override1 (not override0)))"
    },
    {
      "eclass": 119,
      "equivalent": true,
      "id": "override_2",
      "representative": "(and (and (not reset) override_any) (and override2 (not (or override0 override1))))"
    },
    {
      "eclass": 130,
      "equivalent": true,
      "id": "override_3",
      "representative": "(and (and (not reset) override_any) (and override3 (not (or override0 (or override1 override2)))))"
    },
    {
      "eclass": 143,
      "equivalent": true,
      "id": "override_4",
      "representative": "(and (and (not reset) override_any) (and override4 (not (or override0 (or override1 (or override2 override3))))))"
    },
    {
      "eclass": 158,
      "equivalent": true,
      "id": "override_5",
      "representative": "(and (and (not reset) override_any) (and override5 (not (or override0 (or override1 (or override2 (or override3 override4)))))))"
    },
    {
      "eclass": 175,
      "equivalent": true,
      "id": "override_6",
      "representative": "(and (and (not reset) override_any) (and override6 (not (or override0 (or override1 (or override2 (or override3 (or override4 override5))))))))"
    },
    {
      "eclass": 194,
      "equivalent": true,
      "id": "override_7",
      "representative": "(and (and (not reset) override_any) (and override7 (not (or override0 (or override1 (or override2 (or override3 (or override4 (or override5 override6)))))))))"
    }
  ]
}
```
