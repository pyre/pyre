# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# support
import pyre

# the protocol
from .Tile import Tile


# data tiles on the map
class Map(pyre.flow.product, family="pyre.viz.tiles.map", implements=Tile):
    """
    A data tile with memory from a memory mapped file
    """


# end of file
