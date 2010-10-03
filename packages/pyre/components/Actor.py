# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Requirement import Requirement


class Actor(Requirement):
    """
    The metaclass of components

    {Actor} takes care of all the tasks necessary to convert a component declaration into a
    configurable entity that coöperates fully with the framework
    """

    # types
    from .Role import Role


    # meta methods
    def __new__(cls, name, bases, attributes, *, family=None, implements=None, **kwds):
        """
        Build a new component class record

        parameters:
            {cls}: the metaclass invoked; guaranteed to be a descendant of {Actor}
            {name}, {bases}, {attributes}: the usual class specification
            {family}: the public name of this component class; used to configure it
            {implements}: the tuple of interfaces that this component is known to implement
        """
        # record the public name
        attributes["pyre_family"] = family.split(cls.pyre_SEPARATOR) if family else []
        # build the interface specification
        try:
            interface = cls.pyre_buildImplementationSpecification(bases, implements)
        except cls.ImplementationSpecificationError as error:
            error.name = name
            error.description = "{}: {}".format(name, error.description)
            raise
        # and add it to the attributes
        attributes["pyre_implements"] = interface
        # get my ancestors to build the class record
        component = super().__new__(cls, name, bases, attributes, **kwds)
        # if an interface spec was derivable from the declaration, check interface compatibility 
        if interface:
            # check whether the requirements were implemented correctly
            check = component.pyre_isCompatible(interface)
            if not check:
                raise cls.InterfaceError(component, interface, check)
        # and pass the component on
        return component


    def __init__(self, name, bases, attributes, hidden=False, **kwds):
        """
        Initialize a new component class record
        """
        # initialize the record
        super().__init__(name, bases, attributes, **kwds)

        # ask each local trait to embed itself
        for trait in self.pyre_localTraits:
            trait.pyre_embedLocal(component=self)
        # repeat with the inherited traits
        for trait in self.pyre_inheritedTraits:
            trait.pyre_embedInherited(component=self)

        # if this component class is not hidden
        if not hidden:
            # register it with the executive
            self.pyre_executive.registerComponentClass(self)
        # all done
        return


    def __call__(self, **kwds):
        """
        Initialize a new component instance
        """
        # build the component instance
        component = super().__call__(**kwds)
        # register this instance
        self.pyre_executive.registerComponentInstance(component)
        # all done
        return component


    def __setattr__(self, name, value):
        """
        Trap attribute setting in my class record instances to support setting the default
        value using the natural syntax
        """
        # print("Actor.__setattr__: {!r}<-{!r}".format(name, value))
        # bypass while the class record is being built
        if self.pyre_state is None:
            super().__setattr__(name, value)
            return
        # if we get here, the {Registrar} has marked this instance as registered
        # check whether the name corresponds to a trait
        try:
            trait = self.pyre_getTraitDescriptor(alias=name)
        # if it doesn't, bypass
        except self.TraitNotFoundError as error:
            super().__setattr__(name, value)
            return
        # so, the name resolved to a trait
        # use it to set the value
        trait.__set__(instance=self, value=value)
        # and return
        return


    # implementation details
    @classmethod
    def pyre_buildImplementationSpecification(cls, bases, implements):
        """
        Build a class that describes the implementation requirements imposed on this
        {component}, given its class record and the list of interfaces it {implements}
        """
        # initialize the list of interfaces
        interfaces = []
        # try to understand what the component author specified
        if implements is not None:
            # accumulator for the interfaces {component} doesn't implement correctly
            errors = []
            # if {implements} is a single interface, add it to the pile
            if isinstance(implements, cls.Role):
                interfaces.append(implements)
            # the only legal alternative is an iterable of Interface subclasses
            else:
                try:
                    for interface in implements:
                        # if it's an actual Interface subclass
                        if isinstance(interface, cls.Role):
                            # add it to the pile
                            interfaces.append(interface)
                        # otherwise, place it in the error bin
                        else:
                            errors.append(interface)
                # if {implemenents} is not iterable
                except TypeError as error:
                    # put it in the error bin
                    errors.append(implements)
            # report the errors we encountered
            if errors:
                raise cls.ImplementationSpecificationError(errors=errors)
        # now, add the commitments made by my immediate ancestors
        interfaces += [
            base.pyre_implements for base in bases
            if isinstance(base, cls) and base.pyre_implements is not None ]
        # bail out if we didn't manage to find eny interfaces
        if not interfaces: return None
        # otherwise, derive an interface from the harvested ones and return it as the
        # implementation specification
        return cls.Role("Interface", tuple(interfaces), dict(), hidden=True)


    # exceptions
    from .exceptions import ImplementationSpecificationError, InterfaceError


# end of file 
