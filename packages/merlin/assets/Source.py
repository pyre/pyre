# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


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
    def identify(self, authority, **kwds):
        """
        Ask {authority} to process a header file
        """
        # attempt to
        try:
            # ask authority for a handler for my type
            handler = authority.source
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(authority=authority)
        # if it does, invoke it
        return handler(**kwds)


# end of file
