# SPDX-FileCopyrightText: © 2025 Michael Bell
# SPDX-License-Identifier: Apache-2.0

from cocotb.triggers import ClockCycles

from tqv_reg import spi_write_cpha0, spi_read_cpha0

class TinyQV:
    def __init__(self, dut):
        self.dut = dut

    async def reset(self):
        # Reset
        self.dut._log.info("Reset")
        self.dut.ena.value = 1
        self.dut.ui_in.value = 0
        self.dut.uio_in.value = 0
        self.dut.rst_n.value = 0
        await ClockCycles(self.dut.clk, 10)
        self.dut.rst_n.value = 1  
        assert self.dut.uio_oe.value == 0b00001000

    async def write_reg(self, reg, value):
        await spi_write_cpha0(self.dut.clk, self.dut.uio_in, reg, value)


    async def read_reg(self, reg):
        return await spi_read_cpha0(self.dut.clk, self.dut.uio_in, self.dut.uio_out, reg, 0)
