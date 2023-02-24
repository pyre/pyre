# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .MemoryType import MemoryType


# an unsigned 32-bit integer
class UInt32(MemoryType):
    """
    The {uint32_t} type specification
    """

    # constants
    ctype = "uint32_t"


# end of file
