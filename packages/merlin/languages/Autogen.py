# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin
# superclass
from .Language import Language


# class declaration
class Autogen(Language, family="merlin.languages.autogen"):
    """
    A category of source artifacts that are templates that expand into other artifacts
    """

    # constants
    name = "autogen"
    # toolchain attributes
    linkable = True # not true, strictly speaking, but some are...
    # source factories
    source = merlin.assets.template

    # user configurable state
    categories = merlin.properties.catalog(schema=merlin.properties.str())
    categories.default = {
        # source suffixes
        "source": [".in"],
    }
    categories.doc = "a map from file categories to a list of suffixes"

    dialect = merlin.properties.str()
    dialect.default = "cmake"
    dialect.validators = merlin.constraints.isMember("cmake")
    dialect.doc = "specify the expansion pattern syntax to apply"


    # merlin hooks
    def identify(self, visitor, **kwds):
        """
        Ask {visitor} to process one of my source files
        """
        # attempt to
        try:
            # ask the {visitor} for a handler for source files of my type
            handler = visitor.autogen
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(visitor=visitor, **kwds)
        # if it does, invoke it
        return handler(language=self, **kwds)


# end of file
