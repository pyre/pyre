# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# access to the framework
import pyre

# superclasses
from ...LibraryInstallation import LibraryInstallation
from ...ToolInstallation import ToolInstallation

# the protocol
from .MPI import MPI


# the base implementation
class Default(
    ToolInstallation, LibraryInstallation, family="pyre.externals.mpi.default", implements=MPI
):
    """
    A generic MPI installation
    """

    # constants
    category = MPI.category
    flavor = category

    # user configurable state
    launcher = pyre.properties.str(default="mpirun")
    launcher.doc = "the name of the launcher of parallel jobs"

    # interface
    @pyre.export
    def machinefile(self, path):
        """
        Build the command line arguments that hand {path}, a file that describes the machine,
        to my launcher
        """
        # the flavor is unknown, so use the spelling that both the hydra launchers of mpich and
        # intel mpi and the launcher of openmpi accept
        return ["-machinefile", str(path)]


# end of file
