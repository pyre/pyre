# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the base implementation
from .Default import Default


# the openblas flavor
class OpenBLAS(Default, family="pyre.externals.blas.openblas"):
    """
    An OpenBLAS installation
    """

    # constants
    flavor = "openblas"


# end of file
