# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Requirement import Requirement


class Actor(Requirement):
    """
    The component metaclass.

    Takes care of all the tasks necessary to convert a component declaration into a
    configurable entity that fully coöperates with the framework

    The correct implementation relies on the coöperation of the trait descriptors and interface
    decorators from pyre.schema to endow the attribute declarations with a _pyre_category that
    enables the trait classification. See pyre.components.Requirement and
    pyre.patterns.AttributeClassifier for the details of how this is accomplished.
    """


    # meta methods
    def __new__(cls, name, bases, attributes, family=None, implements=None, core=None, **kwds):
        """
        Build the class record

        parameters:
            {cls}: the metaclass invoked; guaranteed to be a Requirement descendant
            {name}: the name of the class being built
            {bases}: a tuple of the base classes from which {cls} derives
            {attributes}: a _pyre_AttributeFilter instance with the {cls} attributes

            {implements}: a tuple of the interfaces that this component is known to implement
            {core}: wrap this components around the class {core} that provides interface
                    implementation
        """
        # get my ancestor to build the class record
        component = super().__new__(cls, name, bases, attributes, **kwds)
        # record the family name
        component._pyre_family = family
        # build my implementation specification
        interface = cls._pyre_buildImplementationSpecification(name, component, bases, implements)
        # check whether this component implements its requirements correctly
        if interface:
            check = component.pyre_isCompatible(interface)
            if not check:
                raise cls.InterfaceError(component, interface, check)

        return component


    def __init__(self, name, bases, attributes, **kwds):
        """
        Initialize a new component record
        """
        # initialize the record
        super().__init__(name, bases, attributes, **kwds)
        # register this component class record
        self._pyre_registrar.registerComponentClass(self)
        return


    def __call__(self, **kwds):
        """
        Initialize a new component instance
        """
        # build the instance
        instance = super().__call__(**kwds)
        # register this instance
        self._pyre_registrar.registerComponentInstance(instance)
        # all done
        return instance


    # implementation details
    @classmethod
    def _pyre_buildImplementationSpecification(cls, name, component, bases, implements):
        """
        Build a class that describes the implementation requirements for this component

        This is done by deriving a class out of whatever interfaces are listed explicitly in
        {implements} and the implementation specification of all the ancestors in {bases}

        parameters:
          {component}: the component record we are building
          {bases}: the tuple of direct bases of the component record we are building
          {implements}: the interfaces mentioned in the declaration of this component
        """
        # pull in the Interface class
        from .Interface import Interface
        # the set of interfaces implemented by this component
        interfaces = set()
        # try to understand what the component author specified
        if implements is not None:
            # accumulator for bad interfaces
            errors = []
            # if implements is a single interface, add it to the pile
            # check that implements is a class before feeding it issubclass
            if isinstance(implements, type) and issubclass(implements, Interface):
                interfaces.add(implements)
            else:
                # the only legal alternative is an iterable of Interface descendants
                try:
                    for interface in implements:
                        if issubclass(interface, Interface):
                            interfaces.add(interface)
                        else:
                            errors.append(interface)
                except TypeError:
                    errors.append(implements)
            # report the error we encountered
            if errors:
                raise cls.ImplementationSpecificationError(name, component, errors)
        # now, extract commitments made by my ancestors that are components
        interfaces |= {
            base._pyre_implements for base in bases
            if isinstance(base, cls) and base._pyre_implements is not None }
        # bail out if we couldn't find any interfaces
        if not interfaces:
            return None
        # otherwise, derive a class from them and return it as the implementation specification
        from .Role import Role
        return Role(
            "_pyre_Interface",
            tuple(interfaces), cls._pyre_AttributeFilter(cls._pyre_CLASSIFIER_NAME))


    # exceptions
    from . import ImplementationSpecificationError, InterfaceError


# end of file 
