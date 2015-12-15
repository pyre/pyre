# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
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

    # constants
    category = 'python'

    # user configurable state
    interpreter = pyre.properties.str(default=sys.executable)
    interpreter.doc = 'the name of the interpreter; may be the full path to the executable'


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Identify the default python installation
        """
        # grab the support for python 3.x
        from .Python3 import Python3
        # and return it
        return Python3


# end of file
