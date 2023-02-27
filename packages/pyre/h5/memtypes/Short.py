# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre

# superclass
from .MemoryType import MemoryType


# a signed short
class Short(MemoryType):
    """
    The {short int} type specification
    """

    # constants
    ctype = "short int"
    htype = pyre.libh5.datatypes.native.short


# end of file
