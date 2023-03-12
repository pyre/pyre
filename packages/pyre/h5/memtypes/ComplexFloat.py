# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
from .. import disktypes

# superclass
from .MemoryType import MemoryType


# a single precision complex number
class ComplexFloat(MemoryType):
    """
    The type specification for single precision complex numbers
    """

    # constants
    ctype = "std::complex<float>"
    htype = disktypes.complexFloat


# the singleton
complexFloat = ComplexFloat()


# end of file
