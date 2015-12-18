# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# framework
import pyre
# superclass
from .Installation import Installation
# my package category
from .MPI import MPI


# the openmpi package manager
class OpenMPI(Installation, family='pyre.externals.openmpi', implements=MPI):
    """
    The package manager for OpenMPI packages
    """

    # public state
    prefix = pyre.properties.str()
    prefix.doc = 'the package installation directory'

    bindir = pyre.properties.str()
    bindir.doc = "the location of my binaries"

    incdir = pyre.properties.str()
    incdir.doc = "the location of my headers; for the compiler command line"

    libdir = pyre.properties.str()
    libdir.doc = "the location of my libraries; for the linker command path"

    launcher = pyre.properties.str(default='mpirun')
    launcher.doc = 'the name of the launcher of MPI jobs'

    # constants
    flavor = "openmpi"
    category = MPI.category


# end of file
