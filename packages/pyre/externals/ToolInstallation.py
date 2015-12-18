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
class ToolInstallation(Installation):
    """
    The package manager for generic tools
    """

    # public state
    bindir = pyre.properties.str()
    bindir.doc = "the location of my binaries"


# end of file
