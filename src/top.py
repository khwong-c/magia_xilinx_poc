from magia import Input, Module, Output, Register


class Top(Module):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.io += [
            Input("GCLK", 1),
            Output("LD", 8),
        ]

        freq_div = Register(24, clk=self.io.GCLK)
        freq_div <<= (freq_div + 1).when(freq_div != (100000000 // 50), 0)

        osc = Register(8, clk=self.io.GCLK, enable=freq_div == 0)
        osc <<= osc + 1
        self.io.LD <<= osc
