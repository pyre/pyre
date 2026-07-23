# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# framework
import pyre

# superclass
from .Installation import Installation


# the base manager of installed libraries
class LibraryInstallation(Installation):
    """
    Base class for installations that provide libraries

    The traits cover everything a build engine needs to assemble compile and link lines:
    compile time markers, compiler flags, include directories, linker flags, library
    directories, the run time search path, and the library stems
    """

    # public state
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

    # framework hooks
    def pyre_configured(self):
        """
        Verify that my {incdir} and {libdir} traits point to good locations
        """
        # chain up
        yield from super().pyre_configured()
        # check that my {incdir} exists
        yield from self.verify(trait="incdir", folders=self.incdir)
        # check that my {libdir} exists
        yield from self.verify(trait="libdir", folders=self.libdir)

        # all done
        return


# end of file
