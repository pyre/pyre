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


    def __new__(cls, name, bases, attributes, implements=None, core=None, **kwds):
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
        # build my implementation specification
        interface = cls._pyre_buildImplementationSpecification(component, bases, implements)
        # check whether this component implements its requirements correctly
        if interface and not component.pyre_isCompatible(interface):
            raise cls.InterfaceError(component, interface)

        return component


    # implementation details
    @classmethod
    def _pyre_buildImplementationSpecification(cls, component, bases, implements):
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


    # exceptions
    from . import InterfaceError

# end of file 
