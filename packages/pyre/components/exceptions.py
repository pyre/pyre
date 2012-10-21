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
        reason = "category mismatch in trait {0.name!r} between {0.configurable} and {0.target}"
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
        msg = '{0.name}: poorly formed implementation specification'
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
            "{{0.component}} does not implement correctly the following protocol{}: {}"
            .format(s, ", ".join(protocols)))
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
        # build the reason
        reason = "{0.configurable} has no trait named {0.name!r}"
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
        reason = "{0.__name__}.{0.trait.name}: could not instantiate {0.value!r}"
        super().__init__(description=reason, **kwds)

        self.configurable = configurable
        self.trait = trait
        self.value = value

        return


# end of file 
