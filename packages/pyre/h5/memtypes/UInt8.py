# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre

# superclass
from .MemoryType import MemoryType


# an unsigned 8-bit integer
class UInt8(MemoryType):
    """
    The {uint8_t} type specification
    """

    # constants
    ctype = "uint8_t"
    htype = pyre.libh5.datatypes.native.uint8


# end of file
