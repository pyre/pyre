# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the base implementation
from .Default import Default


# the openmpi flavor
class OpenMPI(Default, family="pyre.externals.mpi.openmpi"):
    """
    An OpenMPI installation
    """

    # constants
    flavor = "openmpi"

    # interface
    @pyre.export
    def machinefile(self, path):
        """
        Build the command line arguments that hand {path}, a file that describes the machine,
        to my launcher
        """
        # openmpi spells it this way
        return ["--hostfile", str(path)]


# end of file
