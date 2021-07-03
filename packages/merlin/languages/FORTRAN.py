# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


# support
import merlin
# superclass
from .Language import Language


# class declaration
class FORTRAN(Language, family="merlin.languages.fortran"):
    """
    A category of source artifacts encoded in the FORTRAN programming language
    """

    # constants
    name = "FORTRAN"


    # user configurable state
    sources = merlin.properties.strings()
    sources.default = [".f", ".f77", ".f90", ".f95", ".f03", ".F", ".F77", ".F90", ".F95", ".F03"]
    sources.doc = "the set of suffixes that identify an artifact as a source"

    headers = merlin.properties.strings()
    headers.default = [".h", ".inc"]
    headers.doc = "the set of suffixes that identify an artifact as a header"

    modules = merlin.properties.strings()
    modules.default = [".mod"]
    modules.doc = "the set of suffixes that identify an artifact as a module"

    dialects = merlin.properties.strings()
    dialects.default = ["f77", "f95", "f2003", "f2008", "f2018"]
    dialects.doc = "the list of markers that specify supported language dialects"


# end of file
