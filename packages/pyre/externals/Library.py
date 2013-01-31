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
    home = pyre.properties.str() # my installation directory
    incdir = pyre.properties.str() # the location of my header files
    libdir = pyre.properties.str() # my libraries; for LD_LIBRARY_PATH and the link line


    # public data
    @property
    def includes(self):
        """
        Build and return the location of my include files
        """
        # if there is an explicit configuration, use it
        if self.incdir: return self.incdir
        # otherwise, just add "include" to my home
        return os.path.join(self.home, 'include')


    @property
    def libraryPath(self):
        """
        Build an return the location of my libraries
        """
        # if there is an explicit configuration, use it
        if self.libdir: return self.libdir
        # otherwise, just "lib" to my home
        return os.path.join(self.home, 'lib')


    @property
    def libraries(self):
        """
        Return a list of the my libraries that should be included in the link line
        """
        # don't know of any
        return tuple()


# end of file 
