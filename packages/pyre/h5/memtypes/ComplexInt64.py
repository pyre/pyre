# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# a complex number made out of a pair of int64
class ComplexInt64(MemoryType):
    """
    The type specification for int64 complex numbers
    """

    # constants
    ctype = "std::complex<std::int64_t>"
    htype = disktypes.complexFloat


# the singleton
complexInt64 = ComplexInt64()


# end of file
