# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Quantity import Quantity


# the protocol for data tiles
class Tile(Quantity, family="pyre.viz.tiles"):
    """
    The protocol for typed data tiles with a specific storage strategy
    """

    # the c++ product templates whose instantiations satisfy me
    pyre_products = ("pyre::flow::products::tile_t",)

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Provide a default strategy for storing data tiles
        """
        # use the heap
        from ..tiles.Heap import Heap

        # publish
        return Heap


# end of file
