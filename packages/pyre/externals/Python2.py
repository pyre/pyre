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
    The package manager for python 3.x instances
    """

    # public state
    home = pyre.properties.str()
    home.doc = 'the package installation directory'

    requirements = pyre.properties.list(schema=pyre.properties.str())
    requirements.doc = 'the list of package categories on which I depend'

    bin = pyre.properties.str()
    bin.doc = "the location of my binaries"

    lib = pyre.properties.strings()
    lib.doc = "the locations of my libraries; for the linker command path"

    include = pyre.properties.strings()
    include.doc = "the locations of my headers; for the compiler command line"

    path = pyre.properties.strings()
    path.doc = "directories to add to the user's {PATH} environment variable"

    ldpath = pyre.properties.strings()
    ldpath.doc = "directories to add to the user's {LD_LIBRARY_PATH} environment variable"

    interpreter = pyre.properties.str(default=sys.executable)
    interpreter.doc = 'the name of the python interpreter'

    # constants
    category = Python.category


# end of file
