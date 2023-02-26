# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .MemoryType import MemoryType


# a signed byte
class Char(MemoryType):
    """
    The {char} type specification
    """

    # constants
    ctype = "char"


# end of file