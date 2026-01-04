# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclasses
from .Trait import Trait
from ..patterns.Decorator import Decorator


# declaration
class Behavior(Trait, Decorator):
    """
    The base class for component methods that are part of its external interface
    """

    # public data
    method = None  # the actual callable in the component declaration

    # framework data
    # my category name
    category = "behavior"
    # predicate that indicates whether this trait is a behavior
    isBehavior = True

    # metamethods
    def __init__(self, method, tip=None, **kwds):
        # chain up
        super().__init__(method=method, **kwds)
        # save the tip
        self.tip = tip
        # all done
        return

    def __str__(self):
        # build my representation
        return f"'{self.name}': a behavior"


# end of file
