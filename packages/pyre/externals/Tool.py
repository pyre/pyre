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
    bindir = pyre.properties.str()
    bindir.doc = "the location of my binaries"


    # configuration validation
    @classmethod
    def checkBindir(cls, package, filenames):
        """
        Verify that the {bindir} trait points to a good location
        """
        # chain up
        yield from cls.checkFolder(category='bindir', folder=package.bindir, filenames=filenames)
        # all done
        return


# end of file
