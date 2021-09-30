# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .Language import Language


# class declaration
class C(Language, family="merlin.languages.c"):
    """
    A category of source artifacts encoded in the C programming language
    """

    # constants
    name = "c"
    linkable = True


    # user configurable state
    categories = merlin.properties.catalog(schema=merlin.properties.str())
    categories.default = {
        # header suffixes
        "header": [".h"],
        # source suffixes
        "source": [".c"],
    }
    categories.doc = "a map from file categories to a list of suffixes"

    dialect = merlin.properties.str()
    dialect.default = "c99"
    dialect.validators = merlin.constraints.isMember("ansi", "c90", "c99", "c11", "c17", "c18")
    dialect.doc = "the C dialect to enforce"


    # merlin hooks
    def identify(self, authority, **kwds):
        """
        Ask {authority} to process one of my source files
        """
        # attempt to
        try:
            # ask authority for a handler for source files of my type
            handler = authority.c
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(authority=authority, **kwds)
        # if it does, invoke it
        return handler(language=self, **kwds)


# end of file
