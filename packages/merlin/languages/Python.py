# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .Language import Language


# class declaration
class Python(Language, family="merlin.languages.python"):
    """
    A category of source artifacts encoded in the Python programming language
    """

    # constants
    name = "python"


    # user configurable state
    categories = merlin.properties.catalog(schema=merlin.properties.str())
    categories.default = {
        # source suffixes
        "source": [".py"],
    }
    categories.doc = "a map from file categories to a list of suffixes"


    # merlin hooks
    def identify(self, authority, **kwds):
        """
        Ask {authority} to process one of my source files
        """
        # attempt to
        try:
            # ask authority for a handler for source files of my type
            handler = authority.python
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(authority=authority, **kwds)
        # if it does, invoke it
        return handler(language=self, **kwds)


# end of file
