# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# my superclass
from .Shell import Shell


# declaration
class Daemon(Shell):
    """
    A shell that turns a process into a daemon, i.e. a process that is detached from its
    parent and has no access to a terminal
    """

    
    # interface
    def execute(self, *args, **kwds):
        """
        Invoke the application behavior

        For daemons, this is somewhat involved: the process forks twice in order to detach
        itself completely from its parent.
        """
        # NYI! delegate, for now
        return super().execute(*args, **kwds)


# end of file 
