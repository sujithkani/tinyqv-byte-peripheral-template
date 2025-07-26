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

    // PWM duty cycle register
    reg [7:0] duty;

    // 8-bit counter
    reg [7:0] counter;

    // Write duty cycle at address 0
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            duty <= 8'd0;
        else if (data_write && address == 4'h0)
            duty <= data_in;
    end

    // Free-running counter (no reset on write!)
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            counter <= 8'd0;
        else
            counter <= counter + 8'd1;
    end

    // Read-back interface
    assign data_out = (address == 4'h0) ? duty : 8'd0;

    // PWM output: HIGH if counter < duty
    assign uo_out = {7'b0, (counter < duty)};

endmodule
