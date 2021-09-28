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
    sources = merlin.properties.strings()
    sources.default = [".c"]
    sources.doc = "the set of suffixes that identify an artifact as a source"

    headers = merlin.properties.strings()
    headers.default = [".h"]
    headers.doc = "the set of suffixes that identify an artifact as a header"

    dialect = merlin.properties.str()
    dialect.default = "c99"
    dialect.validators = merlin.constraints.isMember("ansi", "c90", "c99", "c11", "c17", "c18")
    dialect.doc = "the C dialect to enforce"


# end of file
