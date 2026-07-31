# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the base implementation
from .Default import Default


# the gsl cblas flavor
class GSLCBLAS(Default, family="pyre.externals.blas.gslcblas"):
    """
    The cblas implementation that ships with GSL
    """

    # constants
    flavor = "gslcblas"


# end of file
