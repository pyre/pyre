# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the base implementation
from .Default import Default


# the atlas flavor
class Atlas(Default, family="pyre.externals.blas.atlas"):
    """
    An ATLAS installation
    """

    # constants
    flavor = "atlas"


# end of file
