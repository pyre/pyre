# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
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
            "category mismatch in trait {!r} between {.pyre_name!r} and {.pyre_name!r}"
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

    def __init__(self, name=None, errors=[], **kwds):
        super().__init__(description="poorly formed implementation specification", **kwds)

        self.name = name
        self.errors = errors

        return


class InterfaceError(ComponentError):
    """
    Exception raised when a component does not implement correctly the interfaces in its
    implementation specification
    """

    def __init__(self, component, interface, report, **kwds):
        # extract the actual interfaces, skipping {object}
        interfaces = tuple(
            "{!r}".format(base.pyre_name)
            for base in interface.__mro__[:-1] if not base.pyre_hidden )
        # support for singular/plural
        s = '' if len(interfaces) == 1 else 's'
        # here is the error description
        reason = (
            "component {.pyre_name!r} does not implement correctly the following interface{}: {}"
            .format(component, s, ", ".join(interfaces)))
        # pass this information along to my superclass
        super().__init__(description=reason, **kwds)
        # and record the error conditions for whomever may be catching this exception
        self.component = component
        self.interface = interface
        self.report = report
        
        return


class TraitNotFoundError(ComponentError):
    """
    Exception raised when a request for a trait fails
    """

    def __init__(self, configurable, name, **kwds):
        # get the family name of the {configurable}
        family = configurable.pyre_getFamilyName()
        # build the family clause of the message
        fclause = ", with family {!r}".format(family) if family else ""
        # build the reason
        reason = "the class {.pyre_name!r}{} has no trait named {!r}".format(
            configurable, fclause, name)
        # pass it on
        super().__init__(description=reason, **kwds)

        # save the source of the error
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
