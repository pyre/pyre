# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# support
import pyre

# the protocol
from .Tile import Tile


# data tiles on the view
class View(pyre.flow.product, family="pyre.viz.tiles.view", implements=Tile):
    """
    A data tile with borrowed memory
    """


# end of file
