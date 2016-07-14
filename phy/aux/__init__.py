from migen.fhdl.std import *
from migen.sim.generic import run_simulation
from migen.genlib.fsm import FSM, NextState, NextValue

class AuxPhy(Module):
    def __init__(self, aux_pads, clk_freq=100000000.):
        self.aux_i = Signal()
        self.aux_o = Signal()
        self.aux_t = Signal()
        self.clk_freq = clk_freq

        txfsm = FSM()

        txfsm.act("IDLE",
            If(!tx_empty, data_sr )
        )
        txfsm.act("PRECHARGE",

        )
        txfsm.act("SYNC",

        )
        txfsm.act("START",

        )
        txfsm.act("SEND_DATA",

        )
        txfsm.act("STOP",

        )
        txfsm.act("FLUSH",

        )
        txfsm.act("WAITING",

        )




