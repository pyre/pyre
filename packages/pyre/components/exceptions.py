# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Definitions for all the exceptions raised by this package
"""


from ..framework.exceptions import FrameworkError


class ComponentError(FrameworkError):
    """
    Base class for component specification errors
    """


class CategoryMismatchError(ComponentError):
    """
    Exception raised when two configurables have traits by the same name but have different
    categories
    """

    def __init__(self, configurable, target, name, **kwds):
        reason = (
            "category mismatch in trait {0!r} between {1.pyre_name!r} and {2.pyre_name!r}"
            .format(name, configurable, target))
        super().__init__(description=reason, **kwds)

        self.configurable = configurable
        self.target = target
        self.name = name

        return


class ImplementationSpecificationError(ComponentError):
    """
    Exception raised when the {implements} specification of a component declaration contains
    errors, e.g. classes that don't derive from Interface
    """

    def __init__(self, name=None, component=None, errors=[], **kwds):
        super().__init__(description="poorly formed implementation specification", **kwds)

        self.component = component
        self.errors = errors

        return


class InterfaceError(ComponentError):
    """
    Exception raised when a component does not implement correctly the interfaces in its
    implementation specification
    """

    def __init__(self, component, interface, report, **kwds):
        reason = (
            "component {0.pyre_name!r} does not implement "
            "interface {1.pyre_name!r} correctly".format(component, interface))
        super().__init__(description=reason, **kwds)
        
        self.component = component
        self.interface = interface
        self.report = report
        
        return


class TraitNotFoundError(ComponentError):
    """
    Exception raised when a request for a trait fails
    """

    def __init__(self, configurable, name, **kwds):
        reason = "{0.pyre_name!r} doesn't have a trait named {1!r}".format(configurable, name)
        super().__init__(description=reason, **kwds)

        self.configurable = configurable
        self.name = name

        return


class FacilitySpecificationError(ComponentError):
    """
    Exception raised when a facility cannot instantiate its configuration specification
    """

    def __init__(self, configurable, trait, value, **kwds):
        reason = "{.pyre_name}.{.name}: could not instantiate {!r}".format(configurable,trait,value)
        super().__init__(description=reason, **kwds)

        self.configurable = configurable
        self.trait = trait
        self.value = value

        return


# end of file 
