# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# an unsigned int
class UnsignedInt(MemoryType):
    """
    The {unsigned int} type specification
    """

    # constants
    ctype = "unsigned int"
    htype = disktypes.unsignedInt


# the singleton
unsignedInt = UnsignedInt()


# end of file
