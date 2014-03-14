# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


# superclass
from .Schema import Schema


# declaration
class Component(Schema):
    """
    A type declarator for components
    """


    # constants
    typename = 'component' # the name of my type
    # types
    from . import uri


    # interface
    def coerce(self, value, **kwds):
        """
        Attempt to convert {value} into a component class compatible with my protocol
        """
        # get my protocol
        protocol = self.protocol
        # which knows the actor type
        actor = protocol.actor
        # and the component type
        component = protocol.component

        # first, give {value} a try
        if isinstance(value, actor) or isinstance(value, component): return value

        # the only remaining case that i can handle is {value} being a string;
        if not isinstance(value, str):
            # build an error message
            msg = 'could not convert {0.value} into a component'
            # and complain, if necessary
            raise self.CastingError(value=value, description=msg) from None
            
        # ok, we have a string; convert it to a uri; if the conversion is not successful, the
        # {uri} schema will complain
        uri = self.uri().coerce(value)
        # extract the fragment, which we use as the instance name; it's ok if it's {None}
        instanceName = uri.fragment
        # extract the address, which we use as the component specification; it's ok if it's {None}
        componentSpec = uri.address
        
        # get the executive
        executive = protocol.pyre_executive
        # and ask it to resolve {value} into component candidates; this will handle correctly
        # uris that resolve to a retrievable component, as well as uris that mention an
        # existing instance
        for candidate in executive.resolve(uri=uri, client=self, **kwds):
            # if it is compatible with my protocol
            if candidate.pyre_isCompatible(protocol):
                # we are done
                return candidate
        # if we have an instance name but no component specification
        if instanceName and not componentSpec:
            # get my default
            default = self.default or protocol.pyre_default()
            # use it to build a component instance
            candidate = default(name=instanceName)
            # and return it
            return candidate
          
        # out of ideas; build an error message
        msg = 'could not convert {0.value} into a component'
        # and complain, if necessary
        raise self.CastingError(value=value, description=msg) from None


    # meta-methods
    def __init__(self, protocol, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my protocol
        self.protocol = protocol
        # all done
        return


# end of file 
