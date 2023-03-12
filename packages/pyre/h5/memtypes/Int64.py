# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# a signed 64-bit integer
class Int64(MemoryType):
    """
    The {int64_t} type specification
    """

    # constants
    ctype = "int64_t"
    htype = disktypes.int64


# the singleton
int64 = Int64()


# end of file
