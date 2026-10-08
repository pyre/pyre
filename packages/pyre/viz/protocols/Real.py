# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Tile import Tile


# a refinement of the tile specification
class Real(Tile, family="pyre.viz.tiles.real"):
    """
    The specification of tiles whose cells hold real values
    """


# end of file
