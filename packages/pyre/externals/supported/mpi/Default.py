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


# end of file
