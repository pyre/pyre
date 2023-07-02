# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Category import Category


# class declaration
class Directory(Category, family="merlin.assets.categories.directory"):
    """
    Encapsulation of a directory as an asset category
    """

    # constants
    category = "directory"

    # interface
    def identify(self, visitor, **kwds):
        """
        Ask {visitor} to process a directory
        """
        # attempt to
        try:
            # ask the {visitor} for a handler for my type
            handler = visitor.directory
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(visitor=visitor, **kwds)
        # if it does, invoke it
        return handler(**kwds)


# end of file
