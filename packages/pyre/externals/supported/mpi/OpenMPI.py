# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the base implementation
from .Default import Default


# the openmpi flavor
class OpenMPI(Default, family="pyre.externals.mpi.openmpi"):
    """
    An OpenMPI installation
    """

    # constants
    flavor = "openmpi"


# end of file
