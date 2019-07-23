# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2019 all rights reserved
#


# externals
import os
# access the framework
import pyre
# get my protocol
from .Terminal import Terminal as terminal
# and the escape sequence helper
from .CSI import CSI


# declaration
class ANSI(pyre.component, family='pyre.terminals.ansi', implements=terminal):
    """
    A terminal that provides color capabilities using ANSI control sequences
    """


    # interface
    def rgb(self, rgb, foreground=True):
        """
        Mix the 6 digit hex string into an ANSI 24-bit color
        """
        # unpack and convert
        red, green, blue = (int(rgb[2*pos:2*(pos+1)], 16) for pos in range(3))
        # build the control sequence
        return CSI.csi24(red=red, green=green, blue=blue, foreground=foreground)


    def rgb256(self, red=0, green=0, blue=0, foreground=True):
        """
        Mix the three digit (r,g,b) base 6 string into an ANSI 256 color
        """
        # build the control sequence
        return CSI.csi8(red=red, green=green, blue=blue, foreground=foreground)


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # figure out the emulation
        self.emulation = os.environ.get('TERM', 'unknown').lower()
        # all done
        return


    ansi = {
        "": "", # no color given
        "none": "", # no color
        "normal": CSI.csi3(code="0"), # reset back to whatever is the default for the terminal

        # regular colors
        "black": CSI.csi3(code="30"),
        "red": CSI.csi3(code="31"),
        "green": CSI.csi3(code="32"),
        "brown": CSI.csi3(code="33"),
        "blue": CSI.csi3(code="34"),
        "purple": CSI.csi3(code="35"),
        "cyan": CSI.csi3(code="36"),
        "light-gray": CSI.csi3(code="37"),

        # bright colors
        "dark-gray": CSI.csi3(bright=True, code="30"),
        "light-red": CSI.csi3(bright=True, code="31"),
        "light-green": CSI.csi3(bright=True, code="32"),
        "yellow": CSI.csi3(bright=True, code="33"),
        "light-blue": CSI.csi3(bright=True, code="34"),
        "light-purple": CSI.csi3(bright=True, code="35"),
        "light-cyan": CSI.csi3(bright=True, code="36"),
        "white": CSI.csi3(bright=True, code="37"),
        }

    x11 = {
    }


# end of file
