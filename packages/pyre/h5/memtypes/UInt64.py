# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre

# superclass
from .MemoryType import MemoryType


# an unsigned 64-bit integer
class UInt64(MemoryType):
    """
    The {uint64_t} type specification
    """

    # constants
    ctype = "uint64_t"
    htype = pyre.libh5.datatypes.native.uint64


# the singleton
uint64 = UInt64()


# end of file
