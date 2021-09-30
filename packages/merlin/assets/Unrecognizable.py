# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .Category import Category


# class declaration
class Unrecognizable(Category, family="merlin.assets.categories.unrecognizable"):
    """
    Encapsulation of a file whose purpose is not known
    """


    # constants
    category = "unrecognizable"


    # interface
    def identify(self, authority, **kwds):
        """
        Ask {authority} to process a file whose category could not be recognized
        """
        # attempt to
        try:
            # ask authority for a handler for my type
            handler = authority.unrecognizable
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(authority=authority, **kwds)
        # if it does, invoke it
        return handler(**kwds)


# end of file
