# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Tile import Tile


# a refinement of the tile specification
class Complex(Tile, family="pyre.viz.tiles.complex"):
    """
    The specification of tiles whose cells hold complex values, such as the samples of a complex raster
    """


# end of file
