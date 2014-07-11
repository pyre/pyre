# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# externals
import itertools
# access to the framework
import pyre
# my protocol
from .Action import Action


# class declaration
class Command(pyre.component, implements=Action):
    """
    A component that implements {Action}
    """


    # public state
    dry = pyre.properties.bool(default=False)
    dry.doc = "show what would get done without actually doing anything"
    

    # expected interface
    @pyre.export
    def main(self, **kwds):
        """
        This is the implementation of the action
        """
        # just print a message
        self.info.log('main: missing implementation')
        # and indicate success
        return 0


    @pyre.export
    def help(self, **kwds):
        """
        Provide help with invoking this action
        """
        # by default, just dump my docstring
        for line in self.__doc__: print(line.strip())
        # and indicate success
        return 0


    # meta-methods
    def __init__(self, name, plexus, **kwds):
        # chain up
        super().__init__(name=name, **kwds)
        # give me journal
        import journal
        # build my channels
        self.debug = plexus.debug
        self.firewall = plexus.firewall
        self.info = plexus.info
        self.warning = plexus.warning
        self.error = plexus.error
        # all done
        return


    # implementation details
    def __call__(self, plexus, argv):
        """
        Commands are callable
        """
        # wire it to invoking {main}
        return self.main(plexus=plexus, argv=argv)

        
# end of file 
