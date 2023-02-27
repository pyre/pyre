# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre

# superclass
from .MemoryType import MemoryType


# a signed long int
class Long(MemoryType):
    """
    The {long int} type specification
    """

    # constants
    ctype = "long int"
    htype = pyre.libh5.datatypes.native.long


# end of file
