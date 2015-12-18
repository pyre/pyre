# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# framework
import pyre
# superclass
from .ToolInstallation import ToolInstallation
from .LibraryInstallation import LibraryInstallation
# my package category
from .MPI import MPI


# the openmpi package manager
class OpenMPI(
        ToolInstallation, LibraryInstallation,
        family='pyre.externals.openmpi', implements=MPI):
    """
    The package manager for OpenMPI packages
    """

    # public state
    launcher = pyre.properties.str(default='mpirun')
    launcher.doc = 'the name of the launcher of MPI jobs'

    # constants
    flavor = "openmpi"
    category = MPI.category


# end of file
