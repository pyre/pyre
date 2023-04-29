# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# an unsigned long int
class UnsignedLong(MemoryType):
    """
    The {unsigned long int} type specification
    """

    # constants
    ctype = "unsigned long int"
    htype = disktypes.unsignedLong


# the singleton
unsignedLong = UnsignedLong()


# end of file
