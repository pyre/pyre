# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# a signed long int
class Long(MemoryType):
    """
    The {long int} type specification
    """

    # constants
    ctype = "long int"
    htype = disktypes.long


# the singleton
long = Long()


# end of file
