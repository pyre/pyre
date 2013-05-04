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


    # constants
    category = 'python'


    # user configurable state
    interpreter = pyre.properties.str()
    interpreter.doc = 'the name of the interpreter; may be the full path to the executable'


# end of file 
