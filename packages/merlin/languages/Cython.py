# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .Language import Language


# class declaration
class Cython(Language, family="merlin.languages.cython"):
    """
    A category of source artifacts encoded in the cython programming language
    """

    # constants
    name = "cython"


    # user configurable state
    categories = merlin.properties.catalog(schema=merlin.properties.str())
    categories.default = {
        # header suffixes
        "header": [".pxi", ".pxd"],
        # source suffixes
        "source": [".pyx"],
    }
    categories.doc = "a map from file categories to a list of suffixes"


# end of file
