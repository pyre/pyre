# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# access to the framework
import pyre
# my base class
from .Executive import Executive


class Script(Executive, family="pyre.shells.script"):
    """
    A shell that invokes the main application behavior and then exits
    """


    # public data
    application = None


    # interface
    @pyre.export
    def run(self, *args, **kwds):
        """
        Invoke the application behavior
        """
        # if i am bound to an application
        if self.application:
            # launch it
            return self.application.main(*args, **kwds)
        # otherwise, just return
        return 0


# end of file 
