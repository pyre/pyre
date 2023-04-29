# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# a signed short
class Short(MemoryType):
    """
    The {short int} type specification
    """

    # constants
    ctype = "short int"
    htype = disktypes.short


# the singleton
short = Short()


# end of file
