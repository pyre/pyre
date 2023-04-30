# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# a double precision floating point number
class Double(MemoryType):
    """
    The {double} type specification
    """

    # constants
    ctype = "double"
    htype = disktypes.double


# the singleton
double = Double()


# end of file
