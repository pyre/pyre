# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# my superclass
from .Daemon import Daemon


# declaration
class Service(Daemon):
    """
    A shell that turns a process into a service harness, i.e. a process that is part of a
    distributed application
    """

    
    # interface
    def execute(self, *args, **kwds):
        """
        Invoke the application behavior
        """
        # NYI! delegate, for now
        return super().execute(*args, **kwds)


# end of file 
