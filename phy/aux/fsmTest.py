from migen.fhdl.std import *
from migen.fhdl import verilog
from migen.genlib.fsm import FSM, NextState, NextValue


class FSMExample(Module):
    def __init__(self):
        self.counter = Signal(8)

        myfsm = FSM()
        self.submodules += myfsm

        self.sync += self.counter.eq(self.counter + 1)
        self.sync += If(self.counter > 235, myfsm.act("COAST",
            If(self.counter == 240, NextState("IDLE"))
        ))
        myfsm.act("IDLE",
            If(self.counter == 10, NextState("START"))
        )
        myfsm.act("START",
            If(self.counter == 100, NextState("RUNNING"))
        )
        myfsm.act("RUNNING",
            If(self.counter == 200, NextState("COAST"))
        )

example = FSMExample()
print(verilog.convert(example))