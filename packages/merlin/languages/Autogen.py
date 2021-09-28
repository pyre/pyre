# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .Language import Language


# class declaration
class Autogen(Language, family="merlin.languages.autogen"):
    """
    A category of source artifacts that are templates that expand into other artifacts
    """

    # constants
    name = "autogen"
    # toolchain attributes
    linkable = True # not true, strictly speaking, but some are...
    # source factories
    source = merlin.assets.template

    # user configurable state
    sources = merlin.properties.strings()
    sources.default = [".in"]
    sources.doc = "the set of suffixes that identify an artifact as a source"

    dialect = merlin.properties.str()
    dialect.default = "cmake"
    dialect.validators = merlin.constraints.isMember("cmake")
    dialect.doc = "specify the expansion pattern syntax to apply"


# end of file
