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

    # interface
    def coerce(self, value, dataset, **kwds):
        """
        Convert {value} into an array
        """
        # this is sufficiently high up in the conversion process to suffice; the only thing higher
        # is {process}, and its implementation in {schema} just delegates to {coerce} immediately;
        # if value is trivial
        if value is self._default:
            # get my shape
            shape = self.shape
            # if it is trivial
            if shape is None:
                # replace it with an empty list
                shape = []
            # otherwise
            else:
                # expand it, replacing unknown extents with zeros
                shape = [0 if s is Ellipsis else s for s in shape]
            # and use it to build a default raster with my memory and on-disk reps
            value = Raster(
                dataset=dataset,
                shape=shape,
                memtype=self.memtype,
                disktype=self.disktype,
            )
        # all done
        return value

    # metamethods
    def __init__(self, chunk=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # record the chunking strategy
        self.chunk = chunk
        # all done
        return

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
        # get the actual shape from the {dataset} value
        space = libh5.DataSpace(shape=dataset.value.shape)
        # i may have a chunking strategy
        chunk = self.chunk
        # hand off the pair
        return type, space, chunk


# end of file
