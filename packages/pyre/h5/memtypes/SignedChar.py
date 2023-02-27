# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre

# superclass
from .MemoryType import MemoryType


# a signed byte
class SignedChar(MemoryType):
    """
    The {signed char} type specification
    """

    # constants
    ctype = "char"
    htype = pyre.libh5.datatypes.native.signedChar


# end of file
