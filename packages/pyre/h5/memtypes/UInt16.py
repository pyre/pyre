# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .MemoryType import MemoryType


# an unsigned 16-bit integer
class UInt16(MemoryType):
    """
    The {uint16_t} type specification
    """

    # constants
    ctype = "uint16_t"


# end of file