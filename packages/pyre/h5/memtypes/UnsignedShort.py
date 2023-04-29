# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# an unsigned short int
class UnsignedShort(MemoryType):
    """
    The {unsigned short int} type specification
    """

    # constants
    ctype = "unsigned short int"
    htype = disktypes.unsignedShort


# the singleton
unsignedShort = UnsignedShort()


# end of file
