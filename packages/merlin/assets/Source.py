# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin
# superclass
from .Category import Category


# class declaration
class Source(Category, family="merlin.assets.categories.source"):
    """
    Encapsulation of a source file
    """


    # constants
    category = "source"


    # interface
    def identify(self, visitor, **kwds):
        """
        Ask {visitor} to process a header file
        """
        # attempt to
        try:
            # ask the {visitor} for a handler for my type
            handler = visitor.source
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(visitor=visitor, **kwds)
        # if it does, invoke it
        return handler(**kwds)


# end of file
