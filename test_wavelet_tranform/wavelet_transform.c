/*
 * SPDX-FileCopyrightText: 2020 Efabless Corporation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * SPDX-License-Identifier: Apache-2.0
 */

#include <defs.h>
#include <stub.c>

// TODO: update with project id from matt
#define PROJECT_ID 0

/*
	IO Test:
		- Configures MPRJ lower 8-IO pins as outputs
		- Observes counter value through the MPRJ lower 8 IO pins (in the testbench)
*/

void main()
{
	/*
	IO Control Registers
	| DM     | VTRIP | SLOW  | AN_POL | AN_SEL | AN_EN | MOD_SEL | INP_DIS | HOLDH | OEB_N | MGMT_EN |
	| 3-bits | 1-bit | 1-bit | 1-bit  | 1-bit  | 1-bit | 1-bit   | 1-bit   | 1-bit | 1-bit | 1-bit   |

	Output: 0000_0110_0000_1110  (0x1808) = GPIO_MODE_USER_STD_OUTPUT
	| DM     | VTRIP | SLOW  | AN_POL | AN_SEL | AN_EN | MOD_SEL | INP_DIS | HOLDH | OEB_N | MGMT_EN |
	| 110    | 0     | 0     | 0      | 0      | 0     | 0       | 1       | 0     | 0     | 0       |


	Input: 0000_0001_0000_1111 (0x0402) = GPIO_MODE_USER_STD_INPUT_NOPULL
	| DM     | VTRIP | SLOW  | AN_POL | AN_SEL | AN_EN | MOD_SEL | INP_DIS | HOLDH | OEB_N | MGMT_EN |
	| 001    | 0     | 0     | 0      | 0      | 0     | 0       | 0       | 0     | 1     | 0       |

	*/

    // i_data_clk
    reg_mprj_io_8 =   GPIO_MODE_USER_STD_INPUT_NOPULL;

    // i_value (8-bit inputs)
    reg_mprj_io_9 =   GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_10 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_11 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_12 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_13 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_14 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_15 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_16 =  GPIO_MODE_USER_STD_INPUT_NOPULL;

    // i_select_output_channel (select up to 2**8=256 channels)
    reg_mprj_io_17 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_18 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_19 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_20 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_21 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_22 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_23 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_24 =  GPIO_MODE_USER_STD_INPUT_NOPULL;

    // o_multiplexed_wavelet_out
    reg_mprj_io_25 =  GPIO_MODE_USER_STD_OUTPUT;
    reg_mprj_io_26 =  GPIO_MODE_USER_STD_OUTPUT;
    reg_mprj_io_27 =  GPIO_MODE_USER_STD_OUTPUT;
    reg_mprj_io_28 =  GPIO_MODE_USER_STD_OUTPUT;
    reg_mprj_io_29 =  GPIO_MODE_USER_STD_OUTPUT;
    reg_mprj_io_30 =  GPIO_MODE_USER_STD_OUTPUT;
    reg_mprj_io_31 =  GPIO_MODE_USER_STD_OUTPUT;
    reg_mprj_io_32 =  GPIO_MODE_USER_STD_OUTPUT;

    // o_active (logical high if module is on)
    reg_mprj_io_33 =  GPIO_MODE_USER_STD_OUTPUT;

    /* Apply configuration */
    reg_mprj_xfer = 1;
    while (reg_mprj_xfer == 1); // waits for io config to complete

    reg_la0_iena = 0; // input enable off
    reg_la0_oenb = 0xffffffff; // enable logic analyser output (ignore the name, 1 is on, 0 off)
    reg_la0_data |= (1 << PROJECT_ID); // enable the project

    // reset
    /* reg_la1_oenb = 1; // is an output */
    // QUESTION: ask about this line
    reg_la1_oenb = 0xffffffff; // is an output
    reg_la1_iena = 0; // is not an input
    reg_la1_data = 1;
    reg_la1_data = 0;

    // no need for anything else as this design is free running.

}

