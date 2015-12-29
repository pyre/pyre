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
class Library(Package):
    """
    Base class for third party libraries
    """

    # user configurable state
    incdir = pyre.properties.strings()
    incdir.doc = "the locations of my headers; for the compiler command line"

    libdir = pyre.properties.strings()
    libdir.doc = "the locations of my libraries; for the linker command path"


    # protocol obligations
    @pyre.export
    def defines(self):
        """
        A sequence of compile time macros that identify my presence
        """


    @pyre.provides
    def headers(self, **kwds):
        """
        A sequence of names of header files to look for
        """


    @pyre.provides
    def liraries(self, **kwds):
        """
        A sequence of names of library files to look for
        """


# end of file
