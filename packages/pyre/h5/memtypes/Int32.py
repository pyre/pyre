# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre

# superclass
from .MemoryType import MemoryType


# a signed 32-bit integer
class Int32(MemoryType):
    """
    The {int32_t} type specification
    """

    # constants
    ctype = "int32_t"
    htype = pyre.libh5.datatypes.native.int32


# the singleton
int32 = Int32()


# end of file
