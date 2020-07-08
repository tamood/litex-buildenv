# Support for the Spartan 3 Starter Kit
from migen import *

from litex.soc.integration.soc import *
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.interconnect import wishbone

from gateware import cas
from gateware import info

from targets.utils import period_ns, dict_set_max
from .crg import _CRG

class BaseSoC(SoCCore):

    def __init__(self, platform, **kwargs):
        kwargs['integrated_rom_size'] = 0x4000
        kwargs['integrated_sram_size'] = 0

        sys_clk_freq = int(50e6)
        # SoCCore ---------------------------------------------------------------------------------
        SoCCore.__init__(self, platform, sys_clk_freq, **kwargs)
        
        # SRAM and Main memory ---------------------------------------------------------------------------------
        self.add_bram("sram", self.mem_map["sram"], 0x800)
        self.add_asram("main_ram", self.mem_map["main_ram"], 0x100000)
        
        # CRG --------------------------------------------------------------------------------------
        self.submodules.crg = _CRG(platform, sys_clk_freq)

        # Basic peripherals ------------------------------------------------------------------------
        #self.submodules.info = info.Info(platform, self.__class__.__name__)
        #self.add_csr("info")
        self.submodules.cas = cas.ControlAndStatus(platform, sys_clk_freq)
        self.add_csr("cas")

    def add_bram(self, name, origin, size, contents=[], mode="rw"):
        ram_bus = wishbone.Interface(data_width=self.bus.data_width)
        ram     = BRAM(size, bus=ram_bus, init=contents, read_only=(mode == "r"))
        self.bus.add_slave(name, ram.bus, SoCRegion(origin=origin, size=size, mode=mode))
        self.check_if_exists(name)
        self.logger.info("RAM {} {} {}.".format(
            colorer(name),
            colorer("added", color="green"),
            self.bus.regions[name]))
        setattr(self.submodules, name, ram)

    def add_asram(self, name, origin, size, contents=[], mode="rw"):
        pads     = self.platform.request("asram")
        asram_bus = wishbone.Interface(data_width=self.bus.data_width)
        self.comb += [ pads.ce0_n.eq(0),
                       pads.ce1_n.eq(0),
                       pads.oe_n.eq(0),
                       pads.adr.eq(asram_bus.adr[:len(pads.adr)]),
                       pads.we_n.eq(~(asram_bus.we & asram_bus.stb & asram_bus.cyc)),
                       pads.sel_n.eq(~asram_bus.sel)]
         # generate ack
        self.sync += [
            asram_bus.ack.eq(0),
            If(asram_bus.cyc & asram_bus.stb & ~asram_bus.ack, asram_bus.ack.eq(1))
        ]              
        for i in range(self.bus.data_width):
                self.specials += Instance("IOBUF", i_I   = asram_bus.dat_w[i], o_O   = asram_bus.dat_r[i], i_T   = ~asram_bus.we & asram_bus.ack, io_IO = pads.dat[i])
                
        self.bus.add_slave(name, asram_bus, SoCRegion(origin=origin, size=size, mode=mode))
        self.check_if_exists(name)
        self.logger.info("RAM {} {} {}.".format(
            colorer(name),
            colorer("added", color="green"),
            self.bus.regions[name]))             

class BRAM(Module):
    def __init__(self, mem_or_size, read_only=None, init=None, bus=None):
        if bus is None:
            bus = Interface()
        self.bus = bus
        bus_data_width = len(self.bus.dat_r)
        if isinstance(mem_or_size, Memory):
            assert(mem_or_size.width <= bus_data_width)
            self.mem = mem_or_size
        else:
            self.mem = Memory(bus_data_width, mem_or_size//(bus_data_width//8), init=init)
        if read_only is None:
            if hasattr(self.mem, "bus_read_only"):
                read_only = self.mem.bus_read_only
            else:
                read_only = False

        ###

        # memory
        port = self.mem.get_port(write_capable=not read_only, we_granularity=bus_data_width,
            mode=READ_FIRST if read_only else WRITE_FIRST)
        self.specials += self.mem, port
        # generate write enable signal
        if not read_only:
            self.comb += [port.we.eq(self.bus.ack & self.bus.we)]
        # address and data
        self.comb += [
            port.adr.eq(self.bus.adr[:len(port.adr)]),
            self.bus.dat_r.eq(port.dat_r)
        ]
        if not read_only:
            self.comb += [port.dat_w[i:i+8].eq(Mux(self.bus.sel[i//8], 
                self.bus.dat_w[i:i+8], port.dat_r[i:i+8])) for i in range(0, bus_data_width, 8)]
        # generate ack
        self.sync += [
            self.bus.ack.eq(0),
            If(self.bus.cyc & self.bus.stb & ~self.bus.ack, self.bus.ack.eq(1))
        ]

SoC = BaseSoC
