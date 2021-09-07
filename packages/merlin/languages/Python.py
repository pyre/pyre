# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .Language import Language


# class declaration
class Python(Language, family="merlin.languages.python"):
    """
    A category of source artifacts encoded in the Python programming language
    """

    # constants
    name = "python"


    # user configurable state
    sources = merlin.properties.strings()
    sources.default = [".py"]
    sources.doc = "the set of suffixes that identify an artifact as a module"

    compiled = merlin.properties.strings()
    compiled.default = [".pyc", ".pyd", ".pyo"]
    compiled.doc = "the set of suffixes that identify an artifact as a byte compiled module"


# end of file
