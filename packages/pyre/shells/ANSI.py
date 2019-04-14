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
        # the plane
        plane = '38' if foreground else '48'
        # unpack and convert
        r, g, b = (int(rgb[2*pos:2*(pos+1)], 16) for pos in range(3))
        # get the code
        return self.csi_color24bit.format(plane, r,g,b)


    def rgb256(self, rgb, foreground=True):
        """
        Mix the three digit (r,g,b) base 6 string into an ANSI 256 color
        """
        # the plane
        plane = '38' if foreground else '48'
        # project
        code = 16 + int(rgb, 6)
        # escape and return
        return self.csi_color256.format(plane, code)


    # meta-methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # figure out the emulation
        self.emulation = os.environ.get('TERM', 'unknown').lower()
        # all done
        return


    # implementation details
    esc = ""
    csi_color8 = esc + "[{}m"
    csi_color256 = esc + "[{};5;{}m"
    csi_color24bit = esc + "[{};2;{};{};{}m"

    colors = {
        "": "", # no color given
        "none": "", # no color
        "normal": csi_color8.format("0"), # reset back to whatever is the default for the terminal

        # regular colors
        "black": csi_color8.format("0;30"),
        "red": csi_color8.format("0;31"),
        "green": csi_color8.format("0;32"),
        "brown": csi_color8.format("0;33"),
        "blue": csi_color8.format("0;34"),
        "purple": csi_color8.format("0;35"),
        "cyan": csi_color8.format("0;36"),
        "light-gray": csi_color8.format("0;37"),

        # bright colors
        "dark-gray": csi_color8.format("1;30"),
        "light-red": csi_color8.format("1;31"),
        "light-green": csi_color8.format("1;32"),
        "yellow": csi_color8.format("1;33"),
        "light-blue": csi_color8.format("1;34"),
        "light-purple": csi_color8.format("1;35"),
        "light-cyan": csi_color8.format("1;36"),
        "white": csi_color8.format("1;37"),
        }


# end of file
