# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# support
import pyre


# the protocol for all raster images
class Raster(pyre.flow.specification, family="pyre.viz.rasters"):
    """
    The raster protocol
    """

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        The default raster
        """
        # use BMP as the default raster
        from .BMP import BMP

        # and return it
        return BMP


# end of file
