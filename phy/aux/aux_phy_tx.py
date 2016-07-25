from migen.fhdl.std import *
from migen.sim.generic import run_simulation
from migen.fhdl import verilog
from migen.actorlib.fifo import SyncFIFO

class AuxPHYTx(Module):
    '''Input ports:
        data_in : 8-bit wide. Data to be pushed into FIFO
        start   : 1-bit wide. Should be high for 1 cycle
                  to start the transmission
        wr_en   : 1-bit wide. Set it high as long as data is pushed into FIFO
                  through data_in port
    Output ports:
        done    : 1-bit wide. Signals completion of transmisison
        full    : 1-bit wide. FIFO is full
        aux_out : 1-bit wide. Actual data transmitted

    NOTE: AuxPHYTx has 16-depth FIFO for storing data for burst transmission.
          For writing into FIFO, set wr_en high and push data through data_in.
          If FIFO becomes full, the full signal will get asserted

    Parameters:
        num_precharge : Number of precharge pulses
        num_sync      : Number of sync pulses
    '''
    def __init__(self, num_precharge=16, num_sync=16):
        # Inputs
        self.data_in = Signal(8)
        self.start = Signal()
        self.wr_en = Signal()

        # Outputs
        self.done = Signal()
        self.full = Signal()
        self.aux_out = Signal()

        # Parameters
        self.num_precharge = num_precharge
        self.num_sync = num_sync

        tx_fifo = SyncFIFO([("data_in", 8)], 16)
