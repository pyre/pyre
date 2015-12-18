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


# the mpich package manager
class LibraryInstallation(Installation):
    """
    The package manager for libraries
    """

    # public state
    incdir = pyre.properties.str()
    incdir.doc = "the location of my headers; for the compiler command line"

    libdir = pyre.properties.str()
    libdir.doc = "the location of my libraries; for the linker command path"


# end of file
