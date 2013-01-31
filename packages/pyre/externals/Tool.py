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
class Tool(Package):
    """
    Base class for external tools
    """


    # user configurable state
    home = pyre.properties.str() # my installation directory
    bindir = pyre.properties.str() # the location of my binaries; we add this to the PATH
    libdir = pyre.properties.str() # the location of my libraries; for LD_LIBRARY_PATH


    # public data
    @property
    def binaries(self):
        """
        Build and return the location of my binary files
        """
        # if there is an explicit configuration, use it
        if self.bindir: return self.bindir
        # otherwise, just add "bin" to my home
        return os.path.join(self.home, 'bin')


    @property
    def libraryPath(self):
        """
        Build an return the location of my libraries
        """
        # if there is an explicit configuration, use it
        if self.libdir: return self.libdir
        # otherwise, just "lib" to my home
        return os.path.join(self.home, 'lib')


# end of file 
