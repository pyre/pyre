# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre

# superclass
from .MemoryType import MemoryType


# an unsigned int
class UnsignedInt(MemoryType):
    """
    The {unsigned int} type specification
    """

    # constants
    ctype = "unsigned int"
    htype = pyre.libh5.datatypes.native.unsignedInt


# end of file
