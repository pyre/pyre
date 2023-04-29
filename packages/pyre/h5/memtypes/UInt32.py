# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# an unsigned 32-bit integer
class UInt32(MemoryType):
    """
    The {uint32_t} type specification
    """

    # constants
    ctype = "uint32_t"
    htype = disktypes.uint32


# the singleton
uint32 = UInt32()


# end of file
