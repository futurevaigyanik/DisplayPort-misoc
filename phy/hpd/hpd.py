from migen.fhdl.std import *
from migen.sim.generic import run_simulation

import math

class HPD_Phy(Module):
    def __init__(self, clk_freq=100000000.):
        self.clk_freq = clk_freq
        self.hpd = Signal()
        self.hpd_irq_o = Signal()
        self.hpd_ev_o = Signal()
        
        self.counter = Signal(30)
        count = Signal()
        
        hpd_r = Signal()
        hpd_rr = Signal() 
        self.sync += [ hpd_rr.eq(hpd_r),
                       hpd_r.eq(self.hpd) ]
        self.sync += [ If( (~hpd_r & hpd_rr), count.eq(1), self.counter.eq(0)),
                       If( (hpd_r & ~hpd_rr), count.eq(0)),
                       If( count, self.counter.eq(self.counter + 1)),
                       If( ((math.ceil(0.5e-3*clk_freq) <= self.counter) & (self.counter <= math.ceil(1e-3*clk_freq)) & (hpd_r & ~hpd_rr)),
                            self.hpd_irq_o.eq(1)
                         ),
                       If( (self.counter>= math.ceil(2e-3*clk_freq)), self.hpd_ev_o.eq(1), count.eq(0), self.counter.eq(0) ),
                       If( self.hpd_irq_o, self.hpd_irq_o.eq(0)),
                       If( self.hpd_ev_o, self.hpd_ev_o.eq(0))]
                       
        
    def do_simulation(self, selfp):
        if selfp.simulator.cycle_counter < 10:
            selfp.hpd = 1
        elif 10 < selfp.simulator.cycle_counter < 12+math.ceil(2e-3*self.clk_freq):
            selfp.hpd = 0
        else:
            selfp.hpd = 1
        if selfp.hpd_irq_o or selfp.hpd_ev_o :
            print("SimCounter: {}, HPD: {}, counter: {} irq: {}, ev: {}".format(
                                        selfp.simulator.cycle_counter,
                                        selfp.hpd,
                                        selfp.counter,
                                        selfp.hpd_irq_o,
                                        selfp.hpd_ev_o))
if __name__ == "__main__":
    dut = HPD_Phy(100000)
    run_simulation(dut, vcd_name="my.vcd", ncycles=1200)
