/*
 * Copyright (c) 2025 Sujith Kani
 * SPDX-License-Identifier: Apache-2.0
 */
`default_nettype none
module tqvp_sujith_pwm(
    input clk, rst_n,
    input [7:0] ui_in,        // Unused here, but must be connected.
    output [7:0] uo_out,       // PWM output on uo_out[0], others are 0.
    input [3:0] address,      // 4-bit local address.
    input data_write,   // Write strobe.
    input  [7:0] data_in,      // Data to write.
    output [7:0] data_out      // Data to read.
);
    // Register to store duty cycle (0–255)
    reg [7:0] duty_cycle;
    reg [7:0] pwm_counter;
    // Write to duty_cycle at address 0
    always @(posedge clk) begin
        if(!rst_n) begin
            duty_cycle<=8'd0;
            pwm_counter<=8'd0;
        end 
        else begin
            if (data_write&&address==4'h0)
                duty_cycle<=data_in;
            pwm_counter<=pwm_counter+1;
        end
    end
    // Output PWM signal on uo_out[0]
    assign uo_out[0]=(pwm_counter<duty_cycle)?1'b1:1'b0;
    assign uo_out[7:1]=7'b0;
    // Read current duty cycle from address 0
    assign data_out=(address==4'h0)?duty_cycle:8'h00;
endmodule
