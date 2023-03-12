# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# an unsigned char
class UnsignedChar(MemoryType):
    """
    The {unsigned char} type specification
    """

    # constants
    ctype = "unsigned char"
    htype = disktypes.unsignedChar


# the singleton
unsignedChar = UnsignedChar()


# end of file
