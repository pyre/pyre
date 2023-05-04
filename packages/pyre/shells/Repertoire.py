# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


# access to the framework
import pyre


# class declaration
class Repertoire:
    """
    The manager of the collection of installed actions
    """


    # types
    from ..components.exceptions import ResolutionError


    # interface
    def invoke(self, plexus, action, argv):
        """
        Locate and invoke the named {action}
        """
        # attempt to
        try:
            # resolve the name into an actual command component
            command = self.resolve(plexus=plexus, spec=action)
        # if this failed
        except self.ResolutionError as error:
            # report it
            plexus.error.log(error)
            # and bail
            return 1
        # otherwise, invoke it
        return command(plexus=plexus, argv=argv)


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
