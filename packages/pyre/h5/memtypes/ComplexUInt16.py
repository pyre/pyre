# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# a complex number made out of a pair of uint16
class ComplexUInt16(MemoryType):
    """
    The type specification for uint16 complex numbers
    """

    # constants
    ctype = "std::complex<std::uint16_t>"
    htype = disktypes.complexUInt16


# the singleton
complexUInt16 = ComplexUInt16()


# end of file
