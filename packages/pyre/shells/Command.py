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
        # just print a message
        self.info.log('help: missing implementation')
        # and indicate success
        return 0


    # meta-methods
    def __init__(self, name, **kwds):
        # chain up
        super().__init__(name=name, **kwds)
        # give me journal
        import journal
        # build my channels
        self.info = journal.info(name)
        self.warning = journal.warning(name)
        self.error = journal.error(name)
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
