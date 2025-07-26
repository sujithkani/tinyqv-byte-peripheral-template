# SPDX-FileCopyrightText: © 2025 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
from tqv import TinyQV

PERIPHERAL_NUM = 16

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    clock = Clock(dut.clk, 100, units="ns")  # 10 MHz
    cocotb.start_soon(clock.start())

    tqv = TinyQV(dut, PERIPHERAL_NUM)

    dut._log.info("Reset")
    await tqv.reset()
    dut._log.info("Reset done")

    # Use a small duty cycle to clearly catch the HIGH state early
    await tqv.write_reg(0, 16)
    readback = await tqv.read_reg(0)
    assert readback == 16, f"Expected 16, got {readback}"
    dut._log.info("PWM duty written and verified")

    seen_high = False
    seen_low = False

    for i in range(512):  # Watch enough cycles to see both edges
        await ClockCycles(dut.clk, 1)
        pwm = int(dut.uo_out.value[0])
        if pwm == 1 and not seen_high:
            seen_high = True
            dut._log.info(f"PWM went HIGH at cycle {i}")
        if pwm == 0 and not seen_low:
            seen_low = True
            dut._log.info(f"PWM went LOW at cycle {i}")
        if seen_high and seen_low:
            break

    assert seen_high and seen_low, "PWM did not toggle as expected"
    dut._log.info("PWM toggled successfully — Test passed.")
