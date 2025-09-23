# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# a complex number made out of a pair of int8
class ComplexUInt8(MemoryType):
    """
    The type specification for uint8 complex numbers
    """

    # constants
    ctype = "std::complex<std::uint8_t>"
    htype = disktypes.complexUInt8


# the singleton
complexUInt8 = ComplexUInt8()


# end of file
