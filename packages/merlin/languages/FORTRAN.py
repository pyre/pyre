# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin
# superclass
from .Language import Language


# class declaration
class FORTRAN(Language, family="merlin.languages.fortran"):
    """
    A category of source artifacts encoded in the FORTRAN programming language
    """

    # constants
    name = "fortran"
    linkable = True


    # user configurable state
    categories = merlin.properties.catalog(schema=merlin.properties.str())
    categories.default = {
        # header suffixes
        "header": [".h", ".inc"],
        # source suffixes
        "source": [".f", ".f77", ".f90", ".f95", ".f03", ".F", ".F77", ".F90", ".F95", ".F03"],
    }
    categories.doc = "a map from file categories to a list of suffixes"

    dialect = merlin.properties.str()
    dialect.default = "f95"
    dialect.validators = merlin.constraints.isMember("f77", "f95", "f2003", "f2008", "f2018")
    dialect.doc = "the list of markers that specify supported language dialects"


    # merlin hooks
    def identify(self, visitor, **kwds):
        """
        Ask {visitor} to process one of my source files
        """
        # attempt to
        try:
            # ask the {visitor} for a handler for source files of my type
            handler = visitor.fortran
        # if it doesn't exist
        except AttributeError:
            # chain up
            return super().identify(visitor=visitor, **kwds)
        # if it does, invoke it
        return handler(language=self, **kwds)


# end of file
