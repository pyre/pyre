# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# support
import pyre

# the protocol
from .Raster import Raster as raster


# the implementations
@pyre.foundry(implements=raster, tip="a microsoft v2 BMP raster")
def bmp():
    """ """
    # pull the implementation
    from .BMP import BMP

    # and publish it
    return BMP


# end of file
