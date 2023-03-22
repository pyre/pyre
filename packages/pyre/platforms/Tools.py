# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# the framework
import pyre


# declaration
class Tools(pyre.protocol, family="pyre.platforms.tools"):
    """
    Encapsulation of host specific information
    """

    # framework obligations
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Build the preferred tool set
        """
        # get the posix tools
        from .POSIXTools import POSIXTools

        # and make them the default
        return POSIXTools


# end of file
