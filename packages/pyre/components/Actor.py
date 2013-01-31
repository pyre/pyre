# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import collections
from .. import tracking
# superclass
from .Requirement import Requirement


# class declaration
class Actor(Requirement):
    """
    The metaclass of components

    {Actor} takes care of all the tasks necessary to convert a component declaration into a
    configurable entity that coöperates fully with the framework
    """


    # types
    from .Role import Role
    from .PublicInventory import PublicInventory
    from .PrivateInventory import PrivateInventory
    from .exceptions import ImplementationSpecificationError, ProtocolError


    # meta-methods
    def __new__(cls, name, bases, attributes, *, family=None, implements=None, **kwds):
        """
        Build a new component record

        parameters:
            {cls}: the metaclass invoked; guaranteed to be a descendant of {Actor}
            {name}, {bases}, {attributes}: the usual class specification
            {implements}: the tuple of protocols that this component is known to implement
        """
        # build the protocol specification
        protocol = cls.pyre_buildProtocol(name, bases, implements)

        # build and add the protocol specification to the attributes
        attributes["pyre_implements"] = protocol
        # save the location of the component declaration
        # N.B.: the locator might be incorrect if the metaclass hierarchy gets deeper;
        # e.g. {pyre.shells.Director}, which doesn't override {__new__} so it is not affected.
        attributes["pyre_locator"] = tracking.here(1)

        # get my ancestors to build the class record
        component = super().__new__(cls, name, bases, attributes, **kwds)

        # and pass the component on
        return component


    def __init__(self, name, bases, attributes, *, family=None, **kwds):
        """
        Initialize a new component class record
        """
        # initialize the record
        super().__init__(name, bases, attributes, **kwds)

        # if this is an internal component, there is nothing further to do
        if self.pyre_internal: return

        # pick the appropriate inventory strategy
        visibility = self.PublicInventory if family else self.PrivateInventory
        # and invoke it to register the component class and build its inventory
        visibility.initializeClass(component=self, family=family)

        # get my protocol specification
        protocol = self.pyre_implements
        # if one was derivable from the declaration, check protocol compatibility 
        if protocol:
            # check whether the requirements were implemented correctly
            check = self.pyre_isCompatible(protocol)
            # if not
            if not check:
                # complain
                raise self.ProtocolError(self, protocol, check)

        # all done
        return


    def __call__(self, name=None, locator=None, **kwds):
        """
        Build an instance of one of my classes
        """
        # record the caller's location
        locator = tracking.here(1) if locator is None else locator
        # build the instance
        instance = super().__call__(name=name, locator=locator, **kwds)
        # and return it
        return instance


    def __setattr__(self, name, value):
        """
        Trap attribute setting in my class record instances to support setting the default
        value using the natural syntax
        """
        # print("Actor.__setattr__: {!r}<-{!r}".format(name, value))
        # recognize internal attributes
        if name.startswith('pyre_'):
            # and process them normally
            return super().__setattr__(name, value)
        # for the rest, try to
        try:
            # normalize the name
            name = self.pyre_namemap[name]
        # if it doesn't
        except KeyError:
            # treat as a normal assignment
            return super().__setattr__(name, value)

        # the name refers to one of my traits; find it
        trait = self.pyre_traitmap[name]
        # build an appropriate locator
        locator = tracking.here(level=1)
        # set the priority
        priority = self.pyre_executive.priority.explicit()
        # set the value
        self.pyre_inventory.setTrait(
            trait=trait, strategy=trait.classSlot, 
            value=value, priority=priority, locator=locator)
        # and return
        return


    def __str__(self):
        # get my family name
        family = self.pyre_family()
        # if i gave one, use it
        if family: return 'component {!r}'.format(family)
        # otherwise, use my class name
        return 'component {.__name__!r}'.format(self)


    # implementation details
    @classmethod
    def pyre_buildProtocol(cls, name, bases, implements):
        """
        Build a class that describes the implementation requirements imposed on this
        {component}, given its class record and the list of protocols it {implements}
        """
        # initialize the list of protocols
        protocols = collections.OrderedDict()

        # try to understand what the component author specified
        if implements is not None:
            # accumulator for the protocols {component} doesn't implement correctly
            errors = []
            # if {implements} is a single protocol, add it to the pile
            if isinstance(implements, cls.Role): protocols[implements] = None
            # the only legal alternative is an iterable of {Protocol} subclasses
            else:
                try:
                    for protocol in implements:
                        # if it's an actual {Protocol} subclass
                        if isinstance(protocol, cls.Role):
                            # add it to the pile
                            protocols[protocol] = None
                        # otherwise, place it in the error bin
                        else:
                            errors.append(protocol)
                # if {implemenents} is not iterable
                except TypeError as error:
                    # put it in the error bin
                    errors.append(implements)
            # report the errors we encountered
            if errors: raise cls.ImplementationSpecificationError(name=name, errors=errors)

        # now, add the commitments made by my immediate ancestors
        protocols.update(
            (base.pyre_implements, None) for base in bases
            if isinstance(base, cls) and base.pyre_implements is not None)

        # convert to a tuple
        protocols = tuple(protocols.keys())
        # bail out if we didn't manage to find any protocols
        if not protocols: return None
        # if there is only one protocol on my pile
        if len(protocols) == 1:
            # use it directly
            return protocols[0]
        # otherwise, derive a protocol from the harvested ones and return it as the
        # implementation specification
        return cls.Role("protocol", protocols, dict(), internal=True)


# end of file 
