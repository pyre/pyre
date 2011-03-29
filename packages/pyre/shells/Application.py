# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the framework
import pyre

# access to my metaclass
from .Director import Director


# declaration
class Application(pyre.component, metaclass=Director, hidden=True):
    """
    Base class for top-level application components

    Application streamlines the interaction with the pyre framework
    """


    # per-instance public data
    pyre_filesystem = None # the root of my private filesystem


    @property
    def executive(self):
        """
        Provide access to the pyre executive
        """
        return self.pyre_executive


    @property
    def fileserver(self):
        """
        Easy access to the executive file server
        """
        return self.pyre_executive.fileserver


    # component interface
    @pyre.export
    def main(self, **kwds):
        """
        The main entry point of an application component
        """
        raise NotImplementedError(
            "application {.pyre_name!r} must implement 'main'".format(self))
        

    @pyre.export
    def help(self, **kwds):
        """
        Hook for the application help system
        """
        raise NotImplementedError(
            "application {.pyre_name!r} must implement 'help'".format(self))
        

# end of file 
