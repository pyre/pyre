# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


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
            plexus.error.log(str(error))
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
        name = f"{plexus.pyre_name}.{spec}"
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
