# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# framework
import pyre

# superclass
from .Installation import Installation


# the base manager of installed tools
class ToolInstallation(Installation):
    """
    Base class for installations that provide executables
    """

    # public state
    bindir = pyre.properties.paths()
    bindir.doc = "the locations of my binaries"

    # framework hooks
    def pyre_configured(self):
        """
        Verify that the {bindir} trait points to a good location
        """
        # chain up
        yield from super().pyre_configured()
        # check that my {bindir} exists
        yield from self.verify(trait="bindir", folders=self.bindir)

        # all done
        return


# end of file
