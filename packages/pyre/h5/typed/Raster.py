# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# support
import math
import pyre


# rasters are tied to non-scalar datasets
class Raster:
    """
    The manager of large multidimensional datasets
    """

    # types
    from .Tile import Tile as tile

    @property
    def rank(self):
        """
        Get my rank
        """
        # go straight to the source
        return self._dataset._pyre_id.space.rank

    @property
    def shape(self):
        """
        Get my shape
        """
        # go straight to the source
        return self._dataset._pyre_id.space.shape

    @property
    def disktype(self):
        """
        Get my expected on-disk type
        """
        # easy enough
        return self._dataset._pyre_layout.disktype

    @property
    def memtype(self):
        """
        Get my in-memory type
        """
        # easy enough
        return self._dataset._pyre_layout.memtype

    @property
    def schema(self):
        """
        Get my layout
        """
        # easy enough
        return self._dataset._pyre_layout

    @property
    def type(self):
        """
        Get my actual on-disk type
        """
        # easy enough
        return self._dataset._pyre_id.type

    # interface
    def read(self, shape, origin=None):
        """
        Allocate a buffer of the given {shape} on the heap, optionally initializing it with
        my contents from {origin}
        """
        # get my dataset
        dataset = self._dataset
        # and schema
        layout = dataset._pyre_layout
        # look up the memtype
        memtype = layout.memtype
        # ask it for the memory
        data = memtype.heap(cells=math.prod(shape))
        # get the dataset handle
        hid = self._dataset._pyre_id
        # if it's connected to a source
        if hid is not None:
            # fill it
            hid.read(data=data, memtype=memtype.htype, shape=shape, origin=origin)
        # make a tile and return it
        return self.tile(data=data, type=memtype, origin=origin, shape=shape)

    # metamethods
    def __init__(self, dataset, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my data source
        self._dataset = dataset
        # make a pile for the cached modifications
        self._staged = []
        # all done
        return

    def __str__(self):
        # easy enough
        return "raster"


# end of file
