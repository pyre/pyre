# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import sys
# framework
import pyre
# superclass
from .ToolInstallation import ToolInstallation
from .LibraryInstallation import LibraryInstallation
# my package category
from .Python import Python


# the python 2.x package manager
class Python2(
        ToolInstallation, LibraryInstallation,
        family='pyre.externals.python2', implements=Python):
    """
    The package manager for python 2.x instances
    """

    # constants
    category = Python.category
    flavor = category + '2'

    # public state
    interpreter = pyre.properties.str(default=flavor)
    interpreter.doc = 'the name of the python interpreter'


# end of file
