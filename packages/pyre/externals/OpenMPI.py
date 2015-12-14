# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# framework
import pyre
# superclass
from .MPI import MPI


# the openmpi package manager
class OpenMPI(pyre.component, family='pyre.externals.openmpi', implements=MPI):
    """
    The package manager for OpenMPI packages
    """

    # public state
    home = pyre.properties.str()
    home.doc = 'the package installation directory'

    requirements = pyre.properties.list(schema=pyre.properties.str())
    requirements.doc = 'the list of package categories on which I depend'

    bin = pyre.properties.str()
    bin.doc = "the location of my binaries"

    lib = pyre.properties.strings()
    lib.doc = "the locations of my libraries; for the linker command path"

    include = pyre.properties.strings()
    include.doc = "the locations of my headers; for the compiler command line"

    path = pyre.properties.strings()
    path.doc = "directories to add to the user's {PATH} environment variable"

    ldpath = pyre.properties.strings()
    ldpath.doc = "directories to add to the user's {LD_LIBRARY_PATH} environment variable"

    launcher = pyre.properties.str(default='mpirun')
    launcher.doc = 'the name of the launcher of MPI jobs'

    # constants
    category = MPI.category


# end of file
