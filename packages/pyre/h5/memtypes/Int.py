# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre

# superclass
from .MemoryType import MemoryType


# a signed int
class Int(MemoryType):
    """
    The {int} type specification
    """

    # constants
    ctype = "int"
    htype = pyre.libh5.datatypes.native.int


# the singleton
int = Int()


# end of file
