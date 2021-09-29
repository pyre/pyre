# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


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


# end of file
