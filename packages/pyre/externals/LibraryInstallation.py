# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# framework
import pyre
# superclass
from .Installation import Installation


# the base installation manager for libraries
class LibraryInstallation(Installation):
    """
    The package manager for libraries
    """

    # public state
    incdir = pyre.properties.strings()
    incdir.doc = "the locations of my headers; for the compiler command line"

    libdir = pyre.properties.strings()
    libdir.doc = "the locations of my libraries; for the linker command path"


    # configuration
    def macports(self, macports, dynamic=True, **kwds):
        """
        Attempt to repair my configuration
        """
        # chain up
        package, contents = super().macports(macports=macports, **kwds)

        # extract the {incdir}
        self.incdir = set(
            macports.findfirst(target=target, contents=contents)
            for target in self.headers(packager=macports))

        # get the host
        host = self.pyre_host
        # deduce the type of libraries we are looking for
        xform = host.dynamicLibrary if dynamic else host.staticLibrary
        # extract the {libdir}
        self.libdir = set(
            macports.findfirst(target=xform(target), contents=contents)
            for target in self.libraries(packager=macports))

        # all done
        return package, contents


    # framework hooks
    def pyre_configured(self):
        """
        Verify that my {incdir} and {libdir} traits point to good locations
        """
        # chain up
        yield from super().pyre_configured()

        # grab my headers
        headers = self.headers(packager=self.pyre_externals)
        # check my {incdir}
        yield from self.verifyFolder(category='incdir', folder=self.incdir, filenames=headers)

        # grab my libraries
        libraries = self.libraries(packager=self.pyre_externals)
        # check my {libdir}
        yield from self.verifyFolder(category='libdir', folder=self.libdir, filenames=libraries)

        # all done
        return


    # protocol obligations
    @pyre.export
    def defines(self):
        """
        Generate a sequence of compile time macros that identify my presence
        """
        # don't know very much
        return ()


    @pyre.export
    def headers(self, **kwds):
        """
        A sequence of names of header files to look for
        """
        # don't know very much
        return ()


    @pyre.export
    def liraries(self, **kwds):
        """
        A sequence of names of library files to look for
        """
        # don't know very much
        return ()


# end of file
