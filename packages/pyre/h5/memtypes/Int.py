# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# a signed int
class Int(MemoryType):
    """
    The {int} type specification
    """

    # constants
    ctype = "int"
    htype = disktypes.int


# the singleton
int = Int()


# end of file
