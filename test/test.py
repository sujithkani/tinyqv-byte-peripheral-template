# SPDX-FileCopyrightText: © 2025 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

from tqv import TinyQV

PERIPHERAL_NUM = 16  # Peripheral number

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    clock = Clock(dut.clk, 100, units="ns")  # 10 MHz
    cocotb.start_soon(clock.start())

    tqv = TinyQV(dut, PERIPHERAL_NUM)
    await tqv.reset()
    dut._log.info("Reset done")

    # Set 50% duty cycle (128)
    await tqv.write_reg(0, 128)
    readback = await tqv.read_reg(0)
    assert readback == 128, f"Expected 128, got {readback}"
    dut._log.info("PWM duty written and verified")

    seen_high = False
    seen_low = False
    high_cycles = 0
    low_cycles = 0

    # Immediately sample after write — for 256 cycles
    for i in range(256):
        await ClockCycles(dut.clk, 1)
        pwm = int(dut.uo_out.value[0])
        if pwm == 1:
            high_cycles += 1
            if not seen_high:
                seen_high = True
                dut._log.info(f"PWM went HIGH at cycle {i}")
        else:
            low_cycles += 1
            if not seen_low:
                seen_low = True
                dut._log.info(f"PWM went LOW at cycle {i}")

    # Confirm PWM toggled and duty ratio is close to 50%
    assert seen_high and seen_low, "PWM did not toggle as expected"
    assert abs(high_cycles - low_cycles) <= 4, f"Duty not near 50%: high={high_cycles}, low={low_cycles}"

    dut._log.info(f"PWM toggled: HIGH for {high_cycles} cycles, LOW for {low_cycles} cycles — Test Passed.")
