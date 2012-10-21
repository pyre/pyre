# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
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
            "category mismatch in trait {!r} between {} and {}"
            .format(name, configurable, target))
        super().__init__(description=reason, **kwds)

        self.configurable = configurable
        self.target = target
        self.name = name

        return


class ImplementationSpecificationError(ComponentError):
    """
    Exception raised when the {implements} specification of a component declaration contains
    errors, e.g. classes that don't derive from Protocol
    """

    def __init__(self, name, errors, **kwds):
        msg = '{}: poorly formed implementation specification'.format(name)
        super().__init__(description=msg, **kwds)

        self.name = name
        self.errors = errors

        return


class ProtocolError(ComponentError):
    """
    Exception raised when a component does not implement correctly the protocols in its
    implementation specification
    """

    def __init__(self, component, protocol, report, **kwds):
        # extract the actual protocols, skipping {object}
        protocols = tuple(str(base) for base in protocol.pyre_pedigree)
        # support for singular/plural
        s = '' if len(protocols) == 1 else 's'
        # here is the error description
        reason = (
            "{} does not implement correctly the following protocol{}: {}"
            .format(component, s, ", ".join(protocols)))
        # pass this information along to my superclass
        super().__init__(description=reason, **kwds)
        # and record the error conditions for whomever may be catching this exception
        self.component = component
        self.protocol = protocol
        self.report = report
        
        return


class TraitNotFoundError(ComponentError):
    """
    Exception raised when a request for a trait fails
    """

    def __init__(self, configurable, name, **kwds):
        # get the family name of the {configurable}
        family = configurable.pyre_family()
        # build the family clause of the message
        fclause = ", with family {!r}".format(family) if family else ""
        # build the reason
        reason = "{}{} has no trait named {!r}".format(
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
        reason = "{.__name__}.{.name}: could not instantiate {!r}".format(configurable,trait,value)
        super().__init__(description=reason, **kwds)

        self.configurable = configurable
        self.trait = trait
        self.value = value

        return


# end of file 
