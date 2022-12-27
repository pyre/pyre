# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin
# superclass
from .Language import Language


# class declaration
class CXX(Language, family="merlin.languages.cxx"):
    """
    A category of source artifacts encoded in the C++ programming language
    """

    # constants
    name = "c++"
    linkable = True


    # user configurable state
    categories = merlin.properties.catalog(schema=merlin.properties.str())
    categories.default = {
        # header suffixes
        "header": [".h", ".hpp", ".hxx", ".h++", ".icc"],
        # source suffixes
        "source": [".cc", ".cpp", ".cxx", ".c++", ".C"],
    }
    categories.doc = "a map from file categories to a list of suffixes"

    dialect = merlin.properties.str()
    dialect.default = "c++20"
    dialect.validators = merlin.constraints.isMember(
        "c++98", "c++11", "c++14", "c++17", "c++20", "c++23")
    dialect.doc = "the C++ standard to conform to"


    # merlin hooks
    def identify(self, visitor, **kwds):
        """
        Ask {visitor} to process one of my source files
        """
        # attempt to
        try:
            # ask the {visitor} for a handler for source files of my type
            handler = visitor.cxx
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(visitor=visitor, **kwds)
        # if it does, invoke it
        return handler(language=self, **kwds)


# end of file
