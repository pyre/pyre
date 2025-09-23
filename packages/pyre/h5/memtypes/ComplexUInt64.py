# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# a complex number made out of a pair of uint64
class ComplexUInt64(MemoryType):
    """
    The type specification for uint64 complex numbers
    """

    # constants
    ctype = "std::complex<std::uint64_t>"
    htype = disktypes.complexUInt64


# the singleton
complexUInt64 = ComplexUInt64()


# end of file
