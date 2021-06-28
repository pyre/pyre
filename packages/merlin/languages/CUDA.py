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
    A category of source artifacts encoded in the C programming language
    """

    # constants
    name= "CUDA"


    # user configurable state
    sources = merlin.properties.strings()
    sources.default = [".cu"]
    sources.doc = "the set of suffixes that identify an artifact as a source"

    headers = merlin.properties.strings()
    headers.default = [".h"]
    headers.doc = "the set of suffixes that identify an artifact as a header"


# end of file
