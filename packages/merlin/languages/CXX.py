# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .Language import Language


# class declaration
class CXX(Language, family="merlin.projects.languages.cxx"):
    """
    A category of source artifacts encoded in the C++ programming language
    """

    # user configurable state
    sources = merlin.properties.strings()
    sources.default = ".cc", ".cpp", ".cxx", ".c++"
    sources.doc = "the set of suffixes that identify an artifact as a source"

    headers = merlin.properties.strings()
    headers.default = ".h", ".hpp", ".hxx", ".h++", ".icc"
    headers.doc = "the set of suffixes that identify an artifact as a header"


# end of file
