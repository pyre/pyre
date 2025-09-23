# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# a complex number made out of a pair of uint32
class ComplexUInt32(MemoryType):
    """
    The type specification for uint32 complex numbers
    """

    # constants
    ctype = "std::complex<std::uint32_t>"
    htype = disktypes.complexUInt32


# the singleton
complexUInt32 = ComplexUInt32()


# end of file
