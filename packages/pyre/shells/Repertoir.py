# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
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
    def resolve(self, plexus, spec):
        """
        Attempt to locate and instantiate a command with the given {name}
        """
        # get the action protocol
        action = self.protocol
        # coerce the {name} into an actual command component
        component = action.pyre_resolveSpecification(spec=spec)
        # construct the name of the instance
        name = '{.pyre_name}.{}'.format(plexus, spec)
        # instantiate it
        command = component(name=name, spec=spec, plexus=plexus, globalAliases=True)
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
