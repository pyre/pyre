# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# support
import math
import weakref


# rasters are tied to non-scalar datasets
class Raster:
    """
    The manager of large multidimensional datasets
    """

    # types
    from .Tile import Tile as tile

    @property
    def dataset(self):
        """
        Get my dataset
        """
        # go straight to the source
        return self._dataset._pyre_id

    @property
    def rank(self):
        """
        Get my rank
        """
        # go straight to the source
        return len(self.shape)

    @property
    def shape(self):
        """
        Get my shape
        """
        # get my explicit value
        shape = self._shape
        # if it's non-trivial
        if shape is not None:
            # that's the right answer
            return shape
        # otherwise, get my rep on disk
        hid = self.dataset
        # if it's trivial
        if hid is None:
            # send back whatever is recorded in my spec
            return self._dataset.shape
        # if not, look it up
        shape = hid.space.shape
        # cache it
        self._shape = shape
        # and return it
        return shape

    @shape.setter
    def shape(self, shape):
        """
        Set my shape
        """
        # get my on-disk rep
        hid = self.dataset
        # if it is non-trivial
        if hid is not None:
            # disallow setting the shape
            raise RuntimeError(
                "can't set the shape of a raster when attached to a dataset"
            )
        # otherwise, record the new value
        self._shape = shape
        # all done
        return

    @property
    def disktype(self):
        """
        Get my expected on-disk type
        """
        # easy enough
        return self._disktype

    @property
    def memtype(self):
        """
        Get my in-memory type
        """
        # easy enough
        return self._memtype

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

    @property
    def dapl(self):
        """
        The dataset access property list
        """
        # easy enough
        return self._dataset._pyre_id.dapl

    @property
    def dcpl(self):
        """
        The dataset creation property list
        """
        # easy enough
        return self._dataset._pyre_id.dcpl

    @property
    def chunk(self):
        """
        The dataset chunk size
        """
        # easy enough
        return self.dcpl.getChunk(rank=len(self.shape))

    @property
    def filters(self):
        """
        The dataset chunk size
        """
        # easy enough
        return self.dcpl.getFilters()

    # interface
    def read(self, shape=None, origin=None):
        """
        Allocate a buffer of the given {shape} on the heap, optionally initializing it with
        my contents from {origin}
        """
        # normalize the shape
        if shape is None:
            # by setting it to cover my entire contents
            shape = self.shape
        # normalize the origin
        if origin is None:
            # by setting to the beginning, if the user didn't specify otherwise
            origin = [0] * len(shape)
        # look up my in-memory type
        memtype = self.memtype
        # ask it for enough memory to hold the requested data
        data = memtype.heap(cells=math.prod(shape))
        # get my dataset handle
        hid = self._dataset._pyre_id
        # if i'm connected to a source
        if hid is not None:
            # populate my buffer
            hid.read(data=data, memtype=memtype.htype, shape=shape, origin=origin)
        # wrap all this up in a tile and return it
        return self.tile(data=data, type=memtype, origin=origin, shape=shape)

    # metamethods
    def __init__(self, dataset, memtype, disktype, shape=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my data source
        self._dataset = None if dataset is None else weakref.proxy(dataset)
        # my shape
        self._shape = shape
        # and my types
        self._memtype = memtype
        self._disktype = disktype
        # make a pile for the cached modifications
        self._staged = []
        # all done
        return

    def __str__(self):
        # easy enough
        return "raster"


# end of file
