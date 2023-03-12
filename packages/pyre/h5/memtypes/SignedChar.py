# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# a signed byte
class SignedChar(MemoryType):
    """
    The {signed char} type specification
    """

    # constants
    ctype = "char"
    htype = disktypes.signedChar


# the singleton
signedChar = SignedChar()


# end of file
