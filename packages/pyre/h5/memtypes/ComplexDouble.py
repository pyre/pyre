# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import pyre

# superclass
from .MemoryType import MemoryType


# a double precision complex number
class ComplexDouble(MemoryType):
    """
    The type specification for double precision complex numbers
    """

    # constants
    ctype = "std::complex<double>"
    htype = pyre.libh5.datatypes.native.complexDouble


# the singleton
complexDouble = ComplexDouble()


# end of file
