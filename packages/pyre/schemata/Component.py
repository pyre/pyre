# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Schema import Schema


# declaration
class Component(Schema):
    """
    A type declarator for components
    """

    # types
    from . import uri

    # constants
    default = object()
    complaint = "could not coerce {0.value!r} into a component"

    # public data
    protocol = None

    @property
    def typename(self):
        """
        Identify my schema through my protocol
        """
        return self.protocol.pyre_family() or "component"

    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a component class compatible with my protocol
        """
        # get my protocol
        protocol = self.protocol
        # which knows the actor type
        actor = protocol.actor
        # the foundry type
        foundry = protocol.foundry
        # and the factory of its default value
        default = protocol.pyre_default

        # if {value} is a string
        if isinstance(value, str):
            # strip it
            value = value.strip()
            # ask the protocol
            try:
                # to have a pass at resolving the {uri} into a compatible component;
                # this handles both uris that point to a retrievable component and uris that
                # point to existing instances known to the executive
                value = protocol.pyre_resolveSpecification(spec=value, **kwds)
            # if that fails
            except protocol.ResolutionError:
                # another valid possibility is a specification like
                #
                #   --facility=#name
                #
                # which is interpreted as a request to instantiate the default facility value
                # with the given name; convert the {value} into a {uri}; if the conversion is
                # not successful, the {uri} schema will complain
                uri = self.uri().coerce(value)
                # extract the fragment, which we use as the instance name; it's ok if it's {None}
                instanceName = uri.fragment
                # extract the address, which we use as the component specification; it's ok if it's {None}
                componentSpec = uri.address
                # if we have an instance name but no component specification
                if instanceName and not componentSpec:
                    # get my default value
                    factory = self.default()
                    # perhaps it's a foundry
                    if isinstance(factory, foundry):
                        # in which case, invoke it
                        factory = factory()
                    # now, if it is a component constructor
                    if isinstance(factory, actor):
                        # use it to build a component instance
                        value = factory(name=instanceName)
                # out of ideas, so leave the string alone; it will be rejected by the validators

        # if {value} is a subclass of my {protocol}
        if isinstance(value, type(protocol)):
            # ask it for its default value
            value = value.pyre_default()

        # if {value} is my protocol's {pyre_default} class method
        if value == default:
            # evaluate it
            value = value()

        # if {value} is a foundry
        if isinstance(value, foundry):
            # invoke it
            value = value()

        # send it off
        return value

    def string(self, value):
        """
        Render value as a string that can be persisted for later coercion
        """
        # respect {None}
        if value is None:
            # by leaving it alone
            return None
        # my value knows
        return value.pyre_name

    def json(self, value):
        """
        Generate a JSON representation of {value}
        """
        # represent as a string
        return self.string(value)

    # meta-methods
    def __init__(self, protocol, default=default, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # save my protocol
        self.protocol = protocol
        # all done
        return


# end of file
