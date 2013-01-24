# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
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
    # a marker that enables applications to deduce the type of shell that is hosting them
    mode = 'script'


    # interface
    @pyre.export
    def launch(self, application, *args, **kwds):
        """
        Invoke the application behavior
        """
        # launch the application
        return application.main(*args, **kwds)


# end of file 
