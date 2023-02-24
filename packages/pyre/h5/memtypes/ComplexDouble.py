# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .MemoryType import MemoryType


# a double precision complex number
class ComplexDouble(MemoryType):
    """
    The type specification for double precision complex numbers
    """

    # constants
    ctype = "std::complex<double>"


# end of file
