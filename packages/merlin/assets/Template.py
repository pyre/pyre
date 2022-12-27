# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <nichael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin
# superclass
from .Category import Category


# class declaration
class Template(Category, family="merlin.assets.categories.template"):
    """
    Encapsulation of a template file that generates other sources
    """


    # constants
    category = "template"


    # interface
    def identify(self, visitor, **kwds):
        """
        Ask {visitor} to process a template file
        """
        # attempt to
        try:
            # ask the {visitor} for a handler for my type
            handler = visitor.template
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(visitor=visitor, **kwds)
        # if it does, invoke it
        return handler(**kwds)


# end of file
