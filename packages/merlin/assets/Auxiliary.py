# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
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
    def identify(self, authority, **kwds):
        """
        Ask {authority} to process a header file
        """
        # attempt to
        try:
            # ask authority for a handler for my type
            handler = authority.auxiliary
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(authority=authority, **kwds)
        # if it does, invoke it
        return handler(**kwds)


# end of file
