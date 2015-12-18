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


# the openmpi package manager
class Python3(
        ToolInstallation, LibraryInstallation,
        family='pyre.externals.python3', implements=Python):
    """
    The package manager for python 3.x instances
    """

    # constants
    category = Python.category
    flavor = category + '3'


    # public state
    interpreter = pyre.properties.str(default=flavor)
    interpreter.doc = 'the name of the python interpreter'

# end of file
