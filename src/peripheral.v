/*
 * Copyright (c) 2025 Sujith Kani
 * SPDX-License-Identifier: Apache-2.0
 */
`default_nettype none
module tqvp_pwm_sujith (
    input         clk,
    input         rst_n,
    input  [7:0]  ui_in,
    output [7:0]  uo_out,
    input  [3:0]  address,
    input         data_write,
    input  [7:0]  data_in,
    output [7:0]  data_out
);
    reg [7:0] duty;
    reg [7:0] counter;
    // Register interface
    always @(posedge clk) begin
        if (!rst_n) begin
            duty<=8'd0;
        end else if (data_write && address == 4'h0) begin
            duty<=data_in;
        end
    end
    assign data_out = (address == 4'h0) ? duty : 8'd0;
    // 8-bit counter for PWM period
    always @(posedge clk) begin
        if (!rst_n)
            counter<=8'd0;
        else
            counter<=counter+8'd1;
    end
    // PWM output: high when counter < duty
    assign uo_out = {7'd0, counter < duty};
endmodule
