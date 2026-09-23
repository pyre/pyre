# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the base implementation
from .Default import Default


# the mpich flavor
class MPICH(Default, family="pyre.externals.mpi.mpich"):
    """
    An MPICH installation
    """

    # constants
    flavor = "mpich"

    # interface
    @pyre.export
    def machinefile(self, path):
        """
        Build the command line arguments that hand {path}, a file that describes the machine,
        to my launcher
        """
        # hydra spells it this way; recent releases also accept the openmpi spelling, older
        # ones refuse it
        return ["-f", str(path)]


# end of file
