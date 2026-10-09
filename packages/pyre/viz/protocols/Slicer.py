# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the specifications of my slots
from .Tile import Tile


# the protocol of the factories that cut tiles out of a raster
class Slicer(pyre.flow.producer, family="pyre.viz.slicers"):
    """
    The slicer protocol: copy a window of a raster into a tile, which is where the data of a
    pipeline comes from
    """

    # the input
    source = Tile.input()
    source.doc = "the raster to cut the tiles out of"

    # the output
    slice = Tile.output()
    slice.doc = "the tile"

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        The default slicer
        """
        # a window sampled at a stride
        from ..slicers.Slice import Slice

        # and return it
        return Slice


# end of file
