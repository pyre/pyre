# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


# framework
import pyre
# superclass
from .Installation import Installation


# the base installation manager for tools
class ToolInstallation(Installation):
    """
    The package manager for generic tools
    """

    # public state
    bindir = pyre.properties.strings()
    bindir.doc = "the location of my binaries"


    # protocol obligations
    @pyre.export
    def binaries(self, **kwds):
        """
        A sequence of names of binaries to look for
        """
        # must have one
        return ()


    # configuration
    def macports(self, macports, **kwds):
        """
        Attempt to repair my configuration
        """
        # chain up
        package, contents = super().macports(macports=macports, **kwds)

        # extract the {bindir}
        self.bindir = set(
            macports.findfirst(target=target, contents=contents)
            for target in self.binaries(packager=macports))

        # all done
        return package, contents


    # framework hooks
    def pyre_configured(self):
        """
        Verify that the {bindir} trait points to a good location
        """
        # chain up
        yield from super().pyre_configured()
        # grab my binaries
        binaries = self.binaries(packager=self.pyre_externals)
        # check my {bindir}
        yield from self.verifyFolder(category='bindir', folder=self.bindir, filenames=binaries)

        # all done
        return


# end of file
