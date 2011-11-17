# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the framework
import pyre
# my superclass
from .Daemon import Daemon


# declaration
class Service(Daemon, family="pyre.shells.service"):
    """
    A shell that turns a process into a service harness, i.e. a process that is part of a
    distributed application
    """

    
    # interface
    @pyre.export
    def run(self, *args, **kwds):
        """
        Invoke the application behavior
        """


# end of file 
