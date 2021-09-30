# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


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
    def identify(self, authority, **kwds):
        """
        Ask {authority} to process a header file
        """
        # attempt to
        try:
            # ask authority for a handler for my type
            handler = authority.header
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(authority=authority, **kwds)
        # if it does, invoke it
        return handler(**kwds)


# end of file
