# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Definitions for all exceptions raised by this package
"""

# grab the base framework exception
from ..framework.exceptions import FrameworkError


# the local ones
class FlowError(FrameworkError):
    """
    Base class for all flow exceptions
    """

    # public data
    description = "generic flow error: {0.node}"

    # metamethods
    def __init__(self, node=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the error info
        self.node = node
        # all done
        return


class IncompleteFlowError(FlowError):
    """
    Exception raised when a request was made to compute a flow that has unbound products
    """

    # public data
    description = "{0.node}, has encountered unbound products"

    # metamethods
    def __init__(self, traits, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the local info
        self.traits = tuple(traits)
        # all done
        return


class RecipeError(FlowError):
    """
    Base class for the errors raised while editing a recipe
    """

    # public data
    description = "recipe error: {0.node}"


class DuplicateNodeError(RecipeError):
    """
    Exception raised when a recipe is asked to add a node under a name it already uses
    """

    # public data
    description = "the recipe has a node named '{0.node}' already"


class UnknownNodeError(RecipeError):
    """
    Exception raised when a recipe is asked about a node it does not have
    """

    # public data
    description = "the recipe has no node named '{0.node}'"


class UnknownSlotError(RecipeError):
    """
    Exception raised when a recipe is asked to bind a slot its factory does not have
    """

    # public data
    description = "'{0.node}' has no slot '{0.slot}'"

    # metamethods
    def __init__(self, slot, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the name of the slot
        self.slot = slot
        # all done
        return


class IncompatiblePinError(RecipeError):
    """
    Exception raised when a node is pinned to something that does not satisfy its protocol
    """

    # public data
    description = "'{0.node}' cannot be pinned to {0.pin}: it does not satisfy {0.protocol}"

    # metamethods
    def __init__(self, pin, protocol, **kwds):
        # chain up
        super().__init__(**kwds)
        # save what was pinned
        self.pin = pin
        # and what it had to satisfy
        self.protocol = protocol
        # all done
        return


class IncompatibleBindingError(RecipeError):
    """
    Exception raised when a slot is bound to a product whose specification is unrelated to the
    one the slot expects
    """

    # public data
    description = (
        "slot '{0.slot}' of '{0.node}' expects {0.expected}, which is unrelated to {0.offered}"
        " of '{0.product}'"
    )

    # metamethods
    def __init__(self, slot, product, expected, offered, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the slot
        self.slot = slot
        # the product
        self.product = product
        # the specification the slot expects
        self.expected = expected
        # and the one the product has
        self.offered = offered
        # all done
        return


class StagingError(RecipeError):
    """
    Base class for the errors raised while staging a recipe against a catalog
    """

    # public data
    description = "while staging '{0.node}': {0.reason}"

    # metamethods
    def __init__(self, reason, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the reason
        self.reason = reason
        # all done
        return


class NoComponentError(StagingError):
    """
    Exception raised when a factory of a recipe is pinned to nothing and its protocol has no
    default component
    """


class NoEngineError(StagingError):
    """
    Exception raised when no instantiation in the catalog can do the work of a factory, given
    the products its neighbors make
    """


class UnresolvedProductError(StagingError):
    """
    Exception raised when staging cannot tell the type of a product of a recipe
    """


class RealizationError(StagingError):
    """
    Exception raised when a staged recipe cannot be built into a graph: a node the catalog does
    not make, a setting a factory refuses, or a binding it refuses
    """


# end of file
