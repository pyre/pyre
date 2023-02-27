# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre

# superclass
from .MemoryType import MemoryType


# an unsigned short int
class UnsignedShort(MemoryType):
    """
    The {unsigned short int} type specification
    """

    # constants
    ctype = "unsigned short int"
    htype = pyre.libh5.datatypes.native.unsignedShort


# end of file
