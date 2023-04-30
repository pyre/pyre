# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# support
import merlin


# the source control system
class SCS(merlin.protocol, family="merlin.scs"):
    """
    The source control system
    """


    # obligations
    @merlin.provides
    def branch(self, **kwds):
        """
        Deduce the name of the currently active branch
        """


    @merlin.provides
    def version(self, **kwds):
        """
        Extract the project version from the source control metadata
        """


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Specify the default implementation
        """
        # no default source control system
        return None


# end of file
