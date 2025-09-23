# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# a complex number made out of a pair of int32
class ComplexInt32(MemoryType):
    """
    The type specification for int32 complex numbers
    """

    # constants
    ctype = "std::complex<std::int32_t>"
    htype = disktypes.complexInt32


# the singleton
complexInt32 = ComplexInt32()


# end of file
