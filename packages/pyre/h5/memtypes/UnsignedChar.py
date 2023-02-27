# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre

# superclass
from .MemoryType import MemoryType


# an unsigned char
class UnsignedChar(MemoryType):
    """
    The {unsigned char} type specification
    """

    # constants
    ctype = "unsigned char"
    htype = pyre.libh5.datatypes.native.unsignedChar


# end of file
