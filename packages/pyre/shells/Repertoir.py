# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# access to the framework
import pyre


# class declaration
class Repertoir:
    """
    The manager of the collection of installed actions
    """


    # types
    from ..components.exceptions import ResolutionError


    # interface
    def find(self, plexus, name):
        """
        Attempt to locate and instantiate a command with the given {name}
        """
        # get the action protocol
        action = self.protocol
        # coerce the {name} into an actual command component
        component = action.pyre_resolveSpecification(spec=name)
        # construct the name of the instance
        tag = '{.pyre_name}.{}'.format(plexus, name)
        # instantiate it
        command = component(name=tag, globalAliases=True)
        # and return it
        return command


    # meta-methods
    def __init__(self, protocol, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the protocol
        self.protocol = protocol
        # all done
        return


    # implementation details
    # data
    protocol = None
        

# end of file 
