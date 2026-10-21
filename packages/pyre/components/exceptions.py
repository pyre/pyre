# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


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

    # public data
    description = "category mismatch in trait {0.name!r} between {0.configurable} and {0.target}"

    # meta-methods
    def __init__(self, configurable, target, name, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error info
        self.configurable = configurable
        self.target = target
        self.name = name
        # all done
        return


class ImplementationSpecificationError(ComponentError):
    """
    Exception raised when the {implements} specification of a component declaration contains
    errors, e.g. classes that don't derive from Protocol
    """

    # public data
    description = "{0.name}: poorly formed implementation specification"

    # meta-methods
    def __init__(self, name, errors, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error info
        self.name = name
        self.errors = errors
        # all done
        return


class ProtocolError(ComponentError):
    """
    Exception raised when a component does not implement correctly the protocols in its
    implementation specification
    """

    # meta-methods
    def __init__(self, component, protocol, report, **kwds):
        # chain up
        super().__init__(**kwds)
        # and record the error conditions for whomever may be catching this exception
        self.component = component
        self.protocol = protocol
        self.report = report
        # extract the actual protocols, skipping {object}
        protocols = tuple(str(base) for base in protocol.pyre_pedigree)
        # support for singular/plural
        s = "" if len(protocols) == 1 else "s"
        # here is the error description
        self.description = (
            "{{0.component}} does not implement correctly the following protocol{}: {}".format(
                s, ", ".join(protocols)
            )
        )

        # all done
        return


class TraitNotFoundError(ComponentError):
    """
    Exception raised when a request for a trait fails
    """

    # public data
    description = "{0.configurable} has no trait named {0.name!r}"

    # meta-methods
    def __init__(self, configurable, name, **kwds):
        # pass it on
        super().__init__(**kwds)
        # save the source of the error
        self.configurable = configurable
        self.name = name
        # all done
        return


class ProtocolCompatibilityError(ComponentError):
    """
    Exception raised when a configurable is incompatible with a suggested protocol
    """

    # public data
    description = "{0.configurable} is incompatible with {0.protocol}"

    # meta-methods
    def __init__(self, configurable, protocol, **kwds):
        # chain up
        super().__init__(**kwds)
        # store my context
        self.configurable = configurable
        self.protocol = protocol
        # all done
        return


class ResolutionError(ComponentError):
    """
    Exception raised when a protocol cannot resolve a string into a component
    """

    # public data
    description = "could not resolve {0.value!r} into a component that implements {0.protocol}"

    # meta-methods
    def __init__(self, protocol, value, report=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # store my context
        self.protocol = protocol
        self.value = value
        self.report = report
        # all done
        return


class FacilitySpecificationError(ResolutionError):
    """
    Exception raised when a protocol is asked to resolve text that is not a component
    specification, i.e. text that cannot be converted into a uri the framework resolvers accept
    """

    # public data
    description = (
        "could not resolve {0.value!r} into a component that implements {0.protocol}, "
        "since it is not a component specification"
    )


class DefaultError(ComponentError):
    """
    Exception raised when a protocol cannot determine a valid default value
    """

    # public data
    description = "no valid default binding for {0.protocol}"

    # meta-methods
    def __init__(self, protocol, **kwds):
        # chain up
        super().__init__(**kwds)
        # store my context
        self.protocol = protocol
        # all done
        return


class TraitValueError(ComponentError):
    """
    Exception raised when a trait refuses a value; validators are encouraged to raise it, or
    an exception derived from it, and the framework names the trait whose value was refused,
    the component or class it belongs to, and where the value was set
    """

    # public data
    description = "{0.target}: {0.reason}"

    @property
    def target(self):
        """
        Name the trait whose value was refused, and its owner, when the name does not say
        """
        # the owner of a slot in the store is part of the name of the trait
        if self.configurable is None or self.slot.key is not None:
            # so the name is enough
            return self.trait
        # otherwise, the owner is told apart by where it was made: a class where it was
        # declared, an instance where it was built
        made = "declared" if isinstance(self.configurable, type) else "built"
        # so name the trait, its owner, and that place
        return f"'{self.trait}' of {self.configurable}, {made} at {self.configurable.pyre_locator}"

    def repeats(self, other) -> bool:
        """
        Check whether {other} is the same refusal as mine: the same slot refused its value for the
        same reason; every assignment makes a new slot, but a slot whose value is an expression
        may refuse it for another reason once the names it refers to change
        """
        # only another refusal
        if not isinstance(other, TraitValueError):
            # can be the same
            return False
        # by the same slot, for the same reason
        return other.slot is self.slot and other.reason == self.reason

    @property
    def reason(self):
        """
        Explain why the value was refused
        """
        # if whoever refused the value said why
        if self._reason is not None:
            # use it
            return self._reason
        # if the value was refused by another error
        if self.error is not None:
            # it knows why
            return str(self.error)
        # otherwise, there is not much to say
        return f"{self.value!r} is not acceptable"

    # meta-methods
    def __init__(self, value=None, reason=None, trait=None, configurable=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # store my context
        self.value = value
        self.trait = trait
        # the component or class that owns the trait, once whoever reads it says so
        self.configurable = configurable
        # and the slot that holds the value, once the factory of its slots says so
        self.slot = None
        # record the explicit reason; i synthesize one when it's missing
        self._reason = reason
        # all done
        return


class ConfigurationError(ComponentError):
    """
    Exception raised when something bad happens during component configuration
    """

    # public data
    description = "while configuring {0.configurable}:\n    {0.report}"

    @property
    def report(self):
        """
        Splice my errors together
        """
        return "\n    ".join(map(str, self.errors))

    # meta-methods
    def __init__(self, configurable, errors, **kwds):
        # chain up
        super().__init__(**kwds)
        # store my context
        self.configurable = configurable
        self.errors = errors
        # all done
        return


class InitializationError(ComponentError):
    """
    Exception raised when something bad happens during component initialization
    """

    # public data
    description = "while initializing {0.configurable}:\n    {0.report}"

    @property
    def report(self):
        """
        Splice my errors together
        """
        return "\n    ".join(map(str, self.errors))

    # meta-methods
    def __init__(self, configurable, errors, **kwds):
        # chain up
        super().__init__(**kwds)
        # store my context
        self.configurable = configurable
        self.errors = errors
        # all done
        return


# end of file
