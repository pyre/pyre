# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the base implementation
from .Default import Default


# the mpich flavor
class MPICH(Default, family="pyre.externals.hdf5.mpich"):
    """
    An HDF5 installation built against MPICH
    """

    # constants
    flavor = "hdf5-mpich"
    tags = ("parallel", "mpich")


# end of file
