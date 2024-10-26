# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2024 all rights reserved


# support
import pyre


# the protocol for data tiles
class Tile(pyre.flow.specification, family="pyre.viz.tiles"):
    """
    The protocol for typed data tiles with a specific storage strategy
    """

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Provide a default strategy for storing data tiles
        """
        # use the heap
        from .Heap import Heap

        # publish
        return Heap


# end of file
