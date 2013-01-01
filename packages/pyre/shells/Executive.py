# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import re
import sys
import pyre # the framework
import operator
import platform
# my protocol
from .Shell import Shell as shell
# the protocols of my traits
from ..platforms import platform


# declaration
class Executive(pyre.component, family='pyre.shells.executive', implements=shell):
    """
    The base class for hosting strategies
    """


    # user configurable state
    home = pyre.properties.str(default=None)
    home.doc = "the process home directory"

    host = platform()
    host.doc = "information about the host machine"


    # interface
    @pyre.export
    def launch(self, application, *args, **kwds):
        """
        Invoke the application behavior
        """
        # {Executive} is abstract
        raise NotImplementedError("class {.__name__} must implement 'launch'".format(type(self)))


# end of file 
