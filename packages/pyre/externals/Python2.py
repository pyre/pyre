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
from .Python import Python


# the openmpi package manager
class Python2(pyre.component, family='pyre.externals.python2', implements=Python):
    """
    The package manager for python 2.x instances
    """

    # public state
    prefix = pyre.properties.str()
    prefix.doc = 'the package installation directory'

    bindir = pyre.properties.str()
    bindir.doc = "the location of my binaries"

    incdir= pyre.properties.str()
    incdir.doc = "the location of my headers; for the compiler command line"

    libdir = pyre.properties.str()
    libdir.doc = "the location of my libraries; for the linker command path"

    interpreter = pyre.properties.str(default=sys.executable)
    interpreter.doc = 'the name of the python interpreter'

    # constants
    category = Python.category


# end of file
