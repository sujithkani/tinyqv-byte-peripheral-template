# SPDX-FileCopyrightText: © 2025 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

from tqv import TinyQV

# Set peripheral number to 16 (default for first byte peripheral)
PERIPHERAL_NUM = 16

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Start the clock (100 ns = 10 MHz)
    clock = Clock(dut.clk, 100, units="ns")
    cocotb.start_soon(clock.start())

    # Create TinyQV helper
    tqv = TinyQV(dut, PERIPHERAL_NUM)

    # Reset system
    await tqv.reset()

    dut._log.info("Writing PWM duty cycle")

    # Write duty cycle = 128 (50%)
    await tqv.write_reg(0, 128)
    readback = await tqv.read_reg(0)
    assert readback == 128, f"Expected 128, got {readback}"

    # Let it settle (after synchronizers and counter)
    await ClockCycles(dut.clk, 3)

    # Sample the PWM output
    seen_high = False
    seen_low = False

    for _ in range(512):  # Two full PWM cycles
        await ClockCycles(dut.clk, 1)
        pwm = int(dut.uo_out.value[0])
        if pwm == 1 and not seen_high:
            seen_high = True
            dut._log.info("PWM went HIGH")
        if pwm == 0 and not seen_low:
            seen_low = True
            dut._log.info("PWM went LOW")

    # Confirm that output toggled
    assert seen_high and seen_low, "PWM did not toggle as expected"
