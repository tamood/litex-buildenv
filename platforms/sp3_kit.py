from litex.build.generic_platform import *
from litex.build.openocd import OpenOCD
from litex.build.xilinx import XilinxPlatform, XC3SProg, VivadoProgrammer


_io = [
    ("clk50", 0, Pins("T9"), IOStandard("LVCMOS33")),

    ("serial", 0,
        Subsignal("tx", Pins("D5"), IOStandard("LVCMOS33"),
                  Misc("SLEW=FAST")),
        Subsignal("rx", Pins("C5"), IOStandard("LVCMOS33"),
                  Misc("SLEW=FAST"))),

    # Small DIP switches
    # DP1 (user_sw:0) -> DP8 (user_sw:7)
    ("user_sw", 0, Pins("F12"), IOStandard("LVCMOS33")),
    ("user_sw", 1, Pins("G12"), IOStandard("LVCMOS33")),
    ("user_sw", 2, Pins("H14"), IOStandard("LVCMOS33")),
    ("user_sw", 3, Pins("H13"), IOStandard("LVCMOS33")),
    ("user_sw", 4, Pins("J14"), IOStandard("LVCMOS33")),
    ("user_sw", 5, Pins("J13"), IOStandard("LVCMOS33")),
    ("user_sw", 6, Pins("K14"), IOStandard("LVCMOS33")),
    ("user_sw", 7, Pins("K13"), IOStandard("LVCMOS33")),

    # Despite being marked as "sw" these are actually buttons which need
    # debouncing.
    # sw1 (user_btn:0) through sw6 (user_btn:5)
    ("user_btn", 0, Pins("M13"), IOStandard("LVCMOS33")),
    ("user_btn", 1, Pins("M14"), IOStandard("LVCMOS33")),
    ("user_btn", 2, Pins("L13"), IOStandard("LVCMOS33")),
    ("user_btn", 3, Pins("L14"), IOStandard("LVCMOS33")),
    # Use BTN3 as the reset button for now.

    # LEDs 1 through 8
    ("user_led", 0, Pins("K12"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 1, Pins("P14"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 2, Pins("l12"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 3, Pins("N14"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 4, Pins("P13"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 5, Pins("N12"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 6, Pins("P12"), IOStandard("LVCMOS33"), Drive(8)),
    ("user_led", 7, Pins("P11"), IOStandard("LVCMOS33"), Drive(8)),
    
    ("asram", 0,
        Subsignal("adr", Pins(
            "L5	N3	M4	M3	L4	G4	F3	F4	E3	E4	G5	H3	H4	J4	J3	K3	K5	L3"),
            IOStandard("LVCMOS33")),
        Subsignal("ce0_n", Pins("P7"), IOStandard("LVCMOS33")),
        Subsignal("ce1_n", Pins("N5"), IOStandard("LVCMOS33")),
        Subsignal("we_n",  Pins("G3"), IOStandard("LVCMOS33")),
        Subsignal("oe_n",  Pins("K4"), IOStandard("LVCMOS33")),
        Subsignal("dat", Pins(
            "N7	T8	R6	T5	R5	C2	C1	B1	D3	P8	F2	H1	J2	L2	P1	R1	P2	N2	M2	K1	J1	G2	E1	D1	D2	E2	G1	F5	C3	K2	M1	N1"),
            IOStandard("LVCMOS33")),
        Subsignal("sel_n",   Pins("P6 T4 P5 R4"), IOStandard("LVCMOS33"))
    )

]

class Platform(XilinxPlatform):
    name = "sp3_kit"
    default_clk_name = "clk50"
    default_clk_period = 20.0

    def __init__(self, toolchain="ise", programmer="openocd"):
        XilinxPlatform.__init__(self, "XC3S200-FT256-4", _io,
                                toolchain=toolchain)
        self.programmer = programmer

