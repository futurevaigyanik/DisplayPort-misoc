from migen.fhdl.std import *

class HPD(Module):
    def __init__(self, hpd):
        self.hpd = hpd
        self.hpd_irq_o = Signal()
        self.hpd_ev_o = Signal()
        
        counter = Signal(30)
        count = Signal()
        
        hpd_r = Signal()
        hpd_rr = Signal()
        self.sync += [ hpd_rr.eq(self.hpd_r),
                       hpd_r.eq(self.hpd) ]
        self.sync += If( (~hpd_r & hpd_rr), 
                            count.eq(1)
                        )
        self.sync += If( (hpd_r & ~hpd_rr), count.eq(0))
        self.sync += If( count, counter.eq(counter + 1))
        
    
    
