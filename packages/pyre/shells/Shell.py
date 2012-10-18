# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# access to my base class
import pyre


# declaration
class Shell(pyre.protocol, family="pyre.shells"):
    """
    The protocol implemented by the pyre application hosting strategies
    """


    # public data
    home = pyre.properties.str(default=None)
    home.doc = "the process home directory"


    # my default implementation
    @classmethod
    def pyre_default(cls):
        """
        The default shell implementation
        """
        # use {Script}
        from .Script import Script
        return Script


    # interface
    @pyre.provides
    def launch(self, application, *args, **kwds):
        """
        Launch the application
        """


# end of file 
