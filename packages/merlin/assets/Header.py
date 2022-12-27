# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# superclass
from .Auxiliary import Auxiliary


# class declaration
class Header(Auxiliary, family="merlin.assets.categories.header"):
    """
    Encapsulation of a header file
    """


    # constants
    category = "header"


    # interface
    def identify(self, visitor, **kwds):
        """
        Ask {visitor} to process a header file
        """
        # attempt to
        try:
            # ask the {visitor} for a handler for my type
            handler = visitor.header
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(visitor=visitor, **kwds)
        # if it does, invoke it
        return handler(**kwds)


# end of file
