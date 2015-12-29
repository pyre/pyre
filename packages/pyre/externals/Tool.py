# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# access to the framework
import pyre
# superclass
from .Package import Package


# my declaration
class Tool(Package):
    """
    Base class for external tools
    """

    # user configurable state
    bindir = pyre.properties.strings()
    bindir.doc = "the locations of my binaries"


    # obligations
    @pyre.provides
    def binaries(self, **kwds):
        """
        A sequence of names of binaries to look for
        """


# end of file
