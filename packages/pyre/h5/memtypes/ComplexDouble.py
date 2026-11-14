# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
from .. import disktypes

# superclass
from .Complex import Complex


# a double precision complex number
class ComplexDouble(Complex):
    """
    The type specification for double precision complex numbers
    """

    # constants
    ctype = "std::complex<double>"  # my spelling in c++
    htype = disktypes.complexDouble  # my hdf5 type, for the values pyre writes
    part = disktypes.double  # the hdf5 type of each part


# the singleton
complexDouble = ComplexDouble()


# end of file
