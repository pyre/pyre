# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre


# the protocol for all image encoders
class Encoder(pyre.flow.producer, family="pyre.viz.encoders"):
    """
    The image encoder protocol
    """

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        The default encoder
        """
        # use BMP as the default encoder
        from ..encoders.BMP import BMP

        # and return it
        return BMP


# end of file
