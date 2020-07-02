# Support for the Spartan 3 Starter Kit

from migen import *



class _CRG(Module):
    def __init__(self, platform, clk_freq):
        # Clock domains for the system (soft CPU and related components run at).
        self.clock_domains.cd_sys = ClockDomain()
        self.clock_domains.cd_por = ClockDomain(reset_less=True)

        clk50 = platform.request("clk50")
        reset = platform.request("user_btn", 3)
        
        int_rst = Signal(reset=1)
        self.sync.por += int_rst.eq(0)
        self.comb += [
            self.cd_sys.clk.eq(clk50),
            self.cd_por.clk.eq(clk50),
            self.cd_sys.rst.eq(int_rst | reset)
        ]
