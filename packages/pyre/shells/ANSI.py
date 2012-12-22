# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# access the framework
import pyre
# get my protocol
from .Terminal import Terminal as terminal


# declaration
class ANSI(pyre.component, family='pyre.shells.terminals.ansi', implements=terminal):


    # implementation details
    esc = "[{}m"
    colors = {
        "": "", # no color given
        "none": "", # no color
        "normal": esc.format("0"), # reset back to whatever is the default for the terminal

        # regular colors
        "black": esc.format("0;30"),
        "red": esc.format("0;31"),
        "green": esc.format("0;32"),
        "brown": esc.format("0;33"),
        "blue": esc.format("0;34"),
        "purple": esc.format("0;35"),
        "cyan": esc.format("0;36"),
        "light-gray": esc.format("0;37"),

        # bright colors
        "dark-gray": esc.format("1;30"),
        "light-red": esc.format("1;31"),
        "light-green": esc.format("1;32"),
        "yellow": esc.format("1;33"),
        "light-blue": esc.format("1;34"),
        "light-purple": esc.format("1;35"),
        "light-cyan": esc.format("1;36"),
        "white": esc.format("1;37"),
        }

    
# end of file 
