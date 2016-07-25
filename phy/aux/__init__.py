from migen.fhdl.std import *
from migen.sim.generic import run_simulation
from migen.genlib.fsm import FSM, NextState, NextValue
from migen.fhdl import verilog

class AuxPhy(Module):
    def __init__(self, aux_pads=None, clk_freq=100000000.):
        self.aux_i = Signal()
        self.aux_o = Signal()
        self.aux_t = Signal()
        self.clk_freq = clk_freq
        self.aux_pads = aux_pads

        data_sr = Signal(16)
        busy_sr = Signal(16)
        tx_empty = Signal()
        tx_rd_en = Signal()
        rx_reset = Signal()
        tx_rd_data = Signal(8)
        txfsm = FSM()

        txfsm.act("IDLE",
            If(tx_empty == 0, data_sr.eq(0b0101010101010101), busy_sr.eq(0b1111111111111111), NextState("PRECHARGE"))
        )
        txfsm.act("PRECHARGE",

        )
        txfsm.act("SYNC",
            data_sr.eq(0b0101010101010101),
            busy_sr.eq(0b1111111111111111),
            NextState("START")
        )
        txfsm.act("START",
            data_sr.eq(0b1111000000000000),
            busy_sr.eq(0b1111111100000000),
            NextState("SEND_DATA"),
            NextValue(rx_reset, rx_reset.eq(1)),
            NextValue(tx_rd_en, tx_rd_en.eq(1))
        )
        txfsm.act("SEND_DATA",
            data_sr.eq(Cat(~tx_rd_data[0], tx_rd_data[0], ~tx_rd_data[1], tx_rd_data[1], ~tx_rd_data[2], tx_rd_data[2],
                           ~tx_rd_data[3], tx_rd_data[3], ~tx_rd_data[4], tx_rd_data[4], ~tx_rd_data[5], tx_rd_data[5],
                           ~tx_rd_data[6], tx_rd_data[6], ~tx_rd_data[7], tx_rd_data[7])),
            busy_sr.eq(0b1111111111111111),
            If(tx_empty, NextState("STOP")).Else(tx_rd_en.eq(1))
        )
        txfsm.act("STOP",
            data_sr.eq(0b1111000000000000),
            busy_sr.eq(0b1111111100000000),
            NextState("FLUSH"),
        )
        txfsm.act("FLUSH",
            NextState("WAITING")
        )
        txfsm.act("WAITING",

        )

if __name__ == "__main__":
    aux_phy = AuxPhy()
    print(verilog.convert(aux_phy))




