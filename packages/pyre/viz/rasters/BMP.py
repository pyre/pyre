# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# support
import pyre

# the protocol
from .Raster import Raster


# a microsoft v2 BMP raster
class BMP(pyre.flow.product, family="pyre.viz.rasters.bmp", implements=Raster):
    """
    A microsoft v2 BMP raster
    """


# end of file
