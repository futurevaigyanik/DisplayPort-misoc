from migen.fhdl.std import *
from migen.sim.generic import run_simulation

class Aux_Phy(Module):
    def __init__(self, aux_pads, clk_freq=100000000.):
        self.aux_i = Signal()
        self.aux_o = Signal()
        self.aux_t = Signal()
        
        
    
