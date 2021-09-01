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
    name = "C"
    linkable = True


    # user configurable state
    sources = merlin.properties.strings()
    sources.default = [".c"]
    sources.doc = "the set of suffixes that identify an artifact as a source"

    headers = merlin.properties.strings()
    headers.default = [".h"]
    headers.doc = "the set of suffixes that identify an artifact as a header"

    dialects = merlin.properties.strings()
    dialects.default = ["ansi", "c90", "c99", "c11", "c17", "c18"]
    dialects.doc = "the list of markers that specify supported language dialects"


# end of file
