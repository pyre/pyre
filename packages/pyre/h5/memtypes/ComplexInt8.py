# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# a complex number made out of a pair of int8
class ComplexInt8(MemoryType):
    """
    The type specification for int8 complex numbers
    """

    # constants
    ctype = "std::complex<std::int8_t>"
    htype = disktypes.complexFloat


# the singleton
complexInt8 = ComplexInt8()


# end of file
