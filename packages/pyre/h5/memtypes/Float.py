# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .MemoryType import MemoryType


# a single precision floating point number
class Float(MemoryType):
    """
    The {float} type specification
    """

    # constants
    ctype = "float"


# end of file
