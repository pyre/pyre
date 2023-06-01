# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# parts
from .Raster import Raster

# typing
from .. import libh5


# the {array} mixin
class Array:
    """
    Implementation details of the {array} dataset mixin
    """

    # type info
    # metamethods
    def __init__(self, shape=None, **kwds):
        # chain up the mixin hierarchy
        super().__init__(shape=shape, **kwds)
        # if my {shape} is trivial
        if shape is None:
            # the default raster object has a trivial shape
            defaultShape = []
        # otherwise
        else:
            # expand the shape, replacing unknown extents with zeros
            defaultShape = [0 if s is Ellipsis else s for s in shape]
        # build the default raster and attach it
        self._default = Raster(
            dataset=None,
            shape=defaultShape,
            memtype=self.memtype,
            disktype=self.disktype,
        )
        # all done
        return

    # interface
    def coerce(self, value, **kwds):
        """
        Convert {value} into an array
        """
        # this is sufficiently high up in the conversion process to suffice; the only thing higher
        # is {process}, and its implementation in {schema} just delegates to {coerce} immediately;
        # so, leave alone, for now
        return value

    # value synchronization
    def _pyre_pull(self, dataset):
        """
        Build a proxy to help with the file interactions
        """
        # build my value
        value = Raster(
            dataset=dataset,
            shape=dataset._pyre_id.space.shape,
            memtype=self.memtype,
            disktype=self.disktype,
        )
        # and return it
        return value

    def _pyre_push(self, src, dst: libh5.DataSet):
        """
        Push my cache value to disk
        """
        # get the src raster
        raster = src.value
        # prime the work pile
        tiles = raster._staged

        # MGA: 20230530
        #   there was logic here to prime {dst} with the contents of {src} before
        #   any staged tile get written out. this is important for transferring data from
        #   one file to another as derived products are constructed
        #
        #   this requires another look to ensure that it only happens once, but it's not
        #   clear what condition the semaphore should be tied to

        # go through the tiles
        for tile in tiles:
            # get the data
            data = tile.data
            # its in-memory data type
            type = tile.type.htype
            # its origin
            origin = tile.origin
            # and shape
            shape = tile.shape
            # and write it out
            dst.write(data=data, memtype=type, origin=origin, shape=shape)
        # all done
        return

    # information about my on-disk layout
    def _pyre_describe(self, dataset):
        """
        Construct representations for my on-disk datatype and dataspace
        """
        # the type is in my schema
        type = self.disktype
        # get the shape from the {dataset} value
        space = libh5.DataSpace(shape=dataset.value.shape)
        # hand off the pair
        return type, space


# end of file
