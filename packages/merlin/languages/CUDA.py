# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin
# superclass
from .Language import Language


# class declaration
class CUDA(Language, family="merlin.languages.cuda"):
    """
    A category of source artifacts encoded in the CUDA programming language
    """

    # constants
    name = "cuda"
    linkable = True


    # user configurable state
    categories = merlin.properties.catalog(schema=merlin.properties.str())
    categories.default = {
        # header suffixes
        "header": [".h"],
        # source suffixes
        "source": [".cu"],
    }
    categories.doc = "a map from file categories to a list of suffixes"


    # merlin hooks
    def identify(self, visitor, **kwds):
        """
        Ask {visitor} to process one of my source files
        """
        # attempt to
        try:
            # ask the {visitor} for a handler for source files of my type
            handler = visitor.cuda
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(visitor=visitor, **kwds)
        # if it does, invoke it
        return handler(language=self, **kwds)


# end of file
