# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
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
    # Properties don't have this problem, since they ostensibly represent simple types that can
    # be instantiated without substantial penalty for both component classes and their
    # instances.

    # Normally, conversions of configuration settings to appropriate inventory values is
    # handled by a trait's type. For facilities, this is normally a subclass of
    # {Protocol}. {Protocol.pyre_cast} solves the first half of the problem: converting a
    # value in to a component class record. In order to solve the second half, {Facility}
    # registers its {pyre_instantiate} as the slot value processor for traits bound to
    # component instances.


    # types
    from ..schema import uri
    from ..components.Actor import Actor as actor
    from ..components.Component import Component as component
    # exceptions
    from ..schema.exceptions import CastingError


    # public data
    converters = ()
    # framework data
    isConfigurable = True


    # interface
    def coerce(self, value, node, **kwds):
        """
        Convert {value} into a component class
        """
        # {None} is special, leave it alone
        if value is None: return value

        # get my protocol
        protocol = self.schema

        # for each attempt to resolve {value} into something useful
        for candidate in self.resolve(value=value, locator=node.locator):
            # check that the candidate is compatible with my protocol
            if candidate.pyre_isCompatible(protocol):
                # we are done
                return candidate

        # otherwise, we are out of ideas; complain
        msg = "could not convert {!r} into a component".format(value)
        raise self.CastingError(value=value, description=msg)


    def instantiate(self, value, node, **kwds):
        """
        Force the instantiation of {value}
        """
        # {None} is special, leave it alone
        if value is None: return value
        # run the {value} through coercion
        value = self.coerce(value=value, node=node, **kwds)
        # if what I got back is a component instance, we are all done
        if isinstance(value, self.component): return value
        # otherwise, instantiate and return it
        return value(key=node.key, name=None, locator=node.locator)


    def find(self, uri):
        """
        Participate in the search for suitable shelves described by {uri}
        """
        # get my protocol
        protocol = self.schema
        # its family name
        family = protocol.pyre_family()
        # the executive
        executive = protocol.pyre_executive
        # the name server
        ns = executive.nameserver
        # and the file server
        fs = executive.fileserver
        # the name server knows the search path, already a list of uris
        searchpath = ns['pyre.configpath']
        # deduce my context path
        contextpath = [''] if not family else ns.split(family)

        # the choices of leading segments
        roots = (p.address for p in reversed(searchpath))
        # sub-folders built out progressively shorter leading portions of the family name
        folders = (
            fs.join(*contextpath[:marker])
            for marker in reversed(range(0,len(contextpath)+1)))
        # and the address specification from the {uri}
        address = [uri.address]
        # with all possible combinations of these three sequences
        for address in itertools.product(roots, folders, address):
            # build a uri and return it
            yield self.uri(scheme='vfs', address=fs.join(*address))

        # any other ideas?
        return


    def initialize(self, **kwds):
        """
        Attach any metadata harvested by the requirement metaclass

        This gets called by {Requirement}, the metaclass of all configurables, as part of the
        process that constructs the class record.
        """
        # chain up
        super().initialize(**kwds)
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


    def resolve(self, value, locator):
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
        # get my protocol
        protocol = self.schema
        # get the executive; my protocol has access
        executive = protocol.pyre_executive
        # the nameserver
        nameserver = executive.nameserver

        # for each potential resolution of {value} by the executive
        for dscr in executive.retrieveComponentDescriptor(uri=uri, facility=self):
            # if it's neither a component class not a component instance
            if not (isinstance(dscr, actor) or isinstance(dscr, component)):
                # it must be a callable that returns one
                dscr = dscr()
                # if not
                if not (isinstance(dscr, actor) or isinstance(dscr, component)):
                    # it's no good; move on
                    continue
            # if it is a class and we have a request to instantiate
            if instanceName and isinstance(dscr, actor):
                # make a locator
                this = tracking.simple('while resolving {!r}'.format(uri.uri))
                locator = tracking.chain(this=this, next=locator)
                # build it
                dscr = dscr(name=instanceName, locator=locator)
            # give this a try
            yield dscr

        # out of ideas
        return

    
    # support for constructing instance slots
    def instanceSlot(self, model):
        """
        Hook registered with the nameserver that informs it of my macro preference and the
        correct converter to attach to new slots for component classes
        """
        return (self.macro(model=model), self.instantiate)


    def macro(self, model):
        """
        Return my choice of macro processor so the caller can build appropriate slots
        """
        # build interpolations
        return model.interpolation


    # meta methods
    def __init__(self, protocol, default=None, **kwds):
        # reset the default value, if necessary
        default = protocol.pyre_default() if default is None else default
        # chain up
        super().__init__(default=default, **kwds)
        # save my protocol
        self.schema = protocol
        # all done
        return


    def __str__(self):
        return "{0.name}: a facility of type {0.schema}".format(self)


# end of file 
