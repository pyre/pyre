# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# a complex number made out of a pair of int16
class ComplexInt16(MemoryType):
    """
    The type specification for int16 complex numbers
    """

    # constants
    ctype = "std::complex<std::int16_t>"
    htype = disktypes.complexInt16


# the singleton
complexInt16 = ComplexInt16()


# end of file
