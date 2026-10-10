# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre

# the protocol
from ..protocols.Slicer import Slicer

# the specifications of my slots
from ..protocols.Raster import Raster
from ..protocols.Tile import Tile


# the slicer that samples a window of a raster at a stride
class Slice(pyre.flow.factory, family="pyre.viz.slicers.slice", implements=Slicer):
    """
    Copy a window of a raster into a tile: the cell at {row, column} of the tile is the cell of
    the raster at {(origin + {row, column}) * stride}, so {origin} is counted in strides; the
    shape of the window is the shape of the tile
    """

    # user configurable state
    origin = pyre.properties.tuple(schema=pyre.properties.int(), default=(0, 0))
    origin.doc = "the location of the window, counted in strides, one per axis"

    stride = pyre.properties.tuple(schema=pyre.properties.int(), default=(1, 1))
    stride.doc = "the distance between the cells of the raster the window samples, one per axis"

    # the input
    source = Raster.input()
    source.doc = "the raster to cut the tile out of"

    # the output
    slice = Tile.output()
    slice.doc = "the tile"

    # the c++ templates whose instantiations do my work, when a recipe is staged
    pyre_engines = ("pyre::flow::factories::sources::slice_t",)


# end of file
