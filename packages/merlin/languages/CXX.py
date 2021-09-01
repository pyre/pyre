# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


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
    name = "C++"
    linkable = True


    # user configurable state
    sources = merlin.properties.strings()
    sources.default = [".cc", ".cpp", ".cxx", ".c++", ".C"]
    sources.doc = "the set of suffixes that identify an artifact as a source"

    headers = merlin.properties.strings()
    headers.default = [".h", ".hpp", ".hxx", ".h++", ".icc"]
    headers.doc = "the set of suffixes that identify an artifact as a header"

    dialects = merlin.properties.strings()
    dialects.default = ["c++98", "c++11", "c++14", "c++17", "c++20", "c++23"]
    dialects.doc = "the list of markers that specify supported language dialects"


# end of file
