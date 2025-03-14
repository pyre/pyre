# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2025 all rights reserved


# superclass
from .Category import Category


# class declaration
class Auxiliary(Category, family="merlin.assets.categories.auxiliary"):
    """
    The category of auxiliary assets
    """

    # constants
    category = "auxiliary"

    # interface
    def identify(self, visitor, **kwds):
        """
        Ask {visitor} to process an auxiliary file
        """
        # attempt to
        try:
            # ask the {visitor} for a handler for my type
            handler = visitor.auxiliary
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(visitor=visitor, **kwds)
        # if it does, invoke it
        return handler(**kwds)


# end of file
