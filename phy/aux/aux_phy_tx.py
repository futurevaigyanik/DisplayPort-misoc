from migen.fhdl.std import *
from migen.sim.generic import run_simulation
from migen.fhdl import verilog
from migen.actorlib.fifo import SyncFIFO

class AuxPHYTx(Module):
    def __init__(self, num_precharge=16, num_sync=16):
        # Inputs
        self.data_in = Signal(8)
        self.start = Signal()

        # Outputs
        self.done = Signal()
        self.aux_out = Signal()

        # Parameters
        self.num_precharge = num_precharge
        self.num_sync = num_sync

        tx_fifo = SyncFIFO([("data_in", 8)], 16)
