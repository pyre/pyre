# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Slicer import Slicer as slicer


# the implementations
@pyre.foundry(implements=slicer, tip="copy a window of a raster, sampled at a stride, into a tile")
def slice():
    """
    Copy a window of a raster, sampled at a stride, into a tile
    """
    # pull the implementation
    from .Slice import Slice

    # and publish it
    return Slice


# end of file
