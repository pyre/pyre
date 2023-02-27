# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre

# superclass
from .MemoryType import MemoryType


# a signed 16-bit integer
class Int16(MemoryType):
    """
    The {int16_t} type specification
    """

    # constants
    ctype = "int16_t"
    htype = pyre.libh5.datatypes.native.int16


# end of file
