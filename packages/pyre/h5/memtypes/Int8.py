# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .MemoryType import MemoryType


# a signed 8-bit integer
class Int8(MemoryType):
    """
    The {int8_t} type specification
    """

    # constants
    ctype = "int8_t"


# end of file
