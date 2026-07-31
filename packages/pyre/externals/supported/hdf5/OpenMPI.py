# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the base implementation
from .Default import Default


# the openmpi flavor
class OpenMPI(Default, family="pyre.externals.hdf5.openmpi"):
    """
    An HDF5 installation built against OpenMPI
    """

    # constants
    flavor = "hdf5-openmpi"
    tags = ("parallel", "openmpi")


# end of file
