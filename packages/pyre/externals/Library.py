# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# access to the framework
import pyre

# superclass
from .Package import Package


# my declaration
class Library(Package):
    """
    Base class for third party libraries
    """

    # user configurable state
    defines = pyre.properties.strings()
    defines.doc = "the compile time markers that indicate my presence"

    flags = pyre.properties.strings()
    flags.doc = "extra flags for the compile line"

    incdir = pyre.properties.paths()
    incdir.doc = "the locations of my headers; for the compiler command line"

    ldflags = pyre.properties.strings()
    ldflags.doc = "extra flags for the link line"

    libdir = pyre.properties.paths()
    libdir.doc = "the locations of my libraries; for the linker command path"

    rpath = pyre.properties.paths()
    rpath.doc = "the run time search path for my libraries; falls back to {libdir} when empty"

    libraries = pyre.properties.strings()
    libraries.doc = "the library stems to place on the link line"


# end of file
