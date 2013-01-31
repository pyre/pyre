# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import os
import sys
# access to the framework
import pyre
# superclass
from .Tool import Tool
from .Library import Library


# the python package manager
class Python(Tool, Library, family='pyre.externals.python'):
    """
    The package manager for the python interpreter
    """


    # user configurable state
    version = pyre.properties.str() # the version of the interpreter

    # public data
    category = 'python'

    @property
    def executable(self):
        """
        Return the full path to the python interpreter
        """
        # construct and return the path to the interpreter
        return os.path.join(self.binaries, 'python{}'.format(self.version))


    # default package factory
    @classmethod
    def configureDefaultPackage(cls, package, platform):
        """
        Encapsulate the default python interpreter on the given {platform}
        """
        # instantiate using a name derived from my category and the platform name
        python = package

        # if this instance did not end up getting a home directory
        if not python.home:
            # set it using the default system directory
            python.home = platform.systemdirs[0]

        # if we don't have an explicit version
        if not python.version:
            # use the current interpreter
            python.version = "{0.major}.{0.minor}".format(sys.version_info)

        # all done
        return python


# end of file 
