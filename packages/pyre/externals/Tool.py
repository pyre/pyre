# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# externals
import os
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
    bin = pyre.properties.str()
    bin.doc = "the location of my binaries"

    path = pyre.properties.strings()
    path.doc = "directories to add to the user's {PATH} environment variable"

    ldpath = pyre.properties.strings()
    ldpath.doc = "directories to add to the user's {LD_LIBRARY_PATH} environment variable"


# end of file 
