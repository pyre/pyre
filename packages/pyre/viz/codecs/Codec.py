# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# support
import pyre


# the protocol for all image encoders
class Codec(pyre.flow.producer, family="pyre.viz.codecs"):
    """
    The image encoder protocol
    """

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        The default encoder
        """
        # use BMP as the default codec
        from .BMP import BMP

        # and return it
        return BMP


# end of file
