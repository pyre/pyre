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
class GenericMPI(
        ToolInstallation, LibraryInstallation,
        family='pyre.externals.genericmpi', implements=MPI):
    """
    The package manager for OpenMPI packages
    """

    # public state
    bindir = pyre.properties.str(default='/usr/bin')
    bindir.doc = "the location of my binaries"

    incdir = pyre.properties.str(default='/usr/include')
    incdir.doc = "the location of my headers; for the compiler command line"

    libdir = pyre.properties.str(default='/usr/lib')
    libdir.doc = "the location of my libraries; for the linker command path"

    launcher = pyre.properties.str(default='mpirun')
    launcher.doc = 'the name of the launcher of MPI jobs'

    # constants
    flavor = "mpi"
    category = MPI.category


# end of file
