# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import os
# access to the framework
import pyre
# superclass
from .Package import Package


# my declaration
class Library(Package):
    """
    Base class for third party libraries
    """


    # user configurable state
    lib = pyre.properties.strings()
    lib.doc = "the locations of my libraries; for the linker command path"

    include = pyre.properties.strings()
    include.doc = "the locations of my headers; for the compiler command line"

    ldpath = pyre.properties.strings()
    ldpath.doc = "directories to add to the user's {LD_LIBRARY_PATH} environment variable"


# end of file 
