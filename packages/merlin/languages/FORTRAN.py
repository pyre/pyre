# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


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


# end of file
