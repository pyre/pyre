# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .Language import Language


# class declaration
class Cython(Language, family="merlin.projects.languages.cython"):
    """
    A category of source artifacts encoded in the cython programming language
    """

    # constants
    name= "cython"


    # user configurable state
    sources = merlin.properties.strings()
    sources.default = [".pyx"]
    sources.doc = "the set of suffixes that identify an artifact as a source"

    headers = merlin.properties.strings()
    headers.default = [".pxi", ".pxd"]
    headers.doc = "the set of suffixes that identify an artifact as a header"


# end of file
