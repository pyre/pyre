# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import itertools
import collections
from .. import tracking
# superclass
from .Slotted import Slotted


# declaration
class Facility(Slotted):
    """
    The base class for traits that must conform to a given interface
    """


    # Facility is faced with the following problem: the expected results of coercing are
    # different depending on whether the object whose trait is being processed is a component
    # class or a component instance. In the latter case, we want to cast the trait value into
    # an actual component instance that is compatible with the facility requirements; in the
    # former we are happy with either a compatible component declaration or an instance.
    

    # types
    from ..schemata import uri
    from ..components.Actor import Actor as actor
    from ..components.Component import Component as component
    # exceptions
    from ..schemata.exceptions import CastingError


    # public data
    schema = None # component developers must specify the facility schema
    converters = ()


    # interface
    def identify(self, value, **kwds):
        """
        Convert {value} into a component class
        """
        # {None} is special, leave it alone
        if value is None: return value

        # attempt to resolve {value} into something useful
        for candidate in self.resolve(value=value):
            # and return the first successful candidate
            return candidate

        # otherwise, we are out of ideas; complain
        msg = "could not convert {0.value!r} into a component"
        raise self.CastingError(value=value, description=msg)


    def coerce(self, value, node, incognito=False,  **kwds):
        """
        Force the instantiation of {value}
        """
        # {None} is special, leave it alone
        if value is None: return value
        # run the {value} through coercion
        value = self.identify(value=value, node=node, **kwds)
        # if what I got back is a component instance, we are all done
        if isinstance(value, self.component): return value

        # get the key of the node
        key = node.key
        # if I am supposed to name the new component
        name = value.pyre_nameserver.getName(key) if not incognito and key else None

        # otherwise, instantiate and return it
        return value(name=name, locator=node.locator)


    def attach(self, **kwds):
        """
        Attach any metadata harvested by the requirement metaclass

        This gets called by {Requirement}, the metaclass of all configurables, as part of the
        process that constructs the class record.
        """
        # chain up
        super().attach(**kwds)
        # adjust the converters
        if self.converters is not tuple():
            # if the user placed them in a container
            if isinstance(self.converters, collections.Iterable):
                # convert it into a tuple
                self.converters = tuple(self.converters)
            # otherwise
            else:
                # make a tuple out of the lone converter
                self.converters = (self.converters, )
        # all done
        return self


    def resolve(self, value, **kwds):
        """
        Attempt to convert {value} to a component
        """
        # the actor type
        actor = self.actor
        # and the component type
        component = self.component

        # first, give {value} a try
        if isinstance(value, actor) or isinstance(value, component): yield value

        # if that didn't work and {value} is not a string, i am out of ideas
        if not isinstance(value, str): return

        # otherwise, convert it to a uri
        uri = self.uri.coerce(value)
        # extract the fragment, which we use as the instance name; it's ok if it's {None}
        instanceName = uri.fragment
        # extract the address, which we use as the component specification; ok if it's {None}
        componentSpec = uri.address
        # get my protocol
        protocol = self.schema

        # if we have an instance name but no component specification
        if instanceName and not componentSpec and self.default:
            # try instantiating a component using my default
            yield self.default(name=instanceName)

        # get the executive; my protocol has access
        executive = protocol.pyre_executive
        # the nameserver
        nameserver = executive.nameserver

        # for each potential resolution of {value} by the executive
        for candidate in executive.resolve(uri=uri, client=self, **kwds):
            # if it is compatible with my protocol
            if candidate.pyre_isCompatible(self.schema):
                # give it a try
                yield candidate

        # out of ideas
        return


    def convert(self, value):
        """
        Walk {value} through the sequence of registered converters
        """
        # first through mine
        for converter in self.converters: value = converter(value)
        # now, ask the protocol to have a go
        value = self.schema.pyre_convert(value)
        # and return it
        return value


    # class initialization
    def classDefault(self, **kwds):
        """
        Compute an appropriate default value for the given {component} class
        """
        # either my default value or whatever my protocol specifies
        return self.default or self.schema.pyre_default(**kwds)


    # support for constructing instance slots
    def classSlot(self, model):
        """
        Hook registered with the nameserver that informs it of my macro preference and the
        correct converter to attach to new slots for component classes
        """
        return (self.macro(model=model), self.identify)


    def macro(self, model):
        """
        Return my choice of macro processor so the caller can build appropriate slots
        """
        # build interpolations
        return model.interpolation


    # meta methods
    def __init__(self, protocol, default=None, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # save my protocol
        self.schema = protocol
        # all done
        return


    def __str__(self):
        return "{0.name}: a facility of type {0.schema}".format(self)


# end of file 
