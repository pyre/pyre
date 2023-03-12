# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# an unsigned 16-bit integer
class UInt16(MemoryType):
    """
    The {uint16_t} type specification
    """

    # constants
    ctype = "uint16_t"
    htype = disktypes.uint16


# the singleton
uint16 = UInt16()


# end of file
