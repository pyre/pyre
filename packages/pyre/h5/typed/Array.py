# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# parts
from .Raster import Raster


# the {array} mixin
class Array:
    """
    Implementation details of the {array} dataset mixin
    """

    # type info
    # metamethods
    def __init__(self, shape=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the shape
        self.shape = shape
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

    # framework hooks value synchronization
    def _pyre_pull(self, dataset):
        """
        Build a proxy to help with the file interactions
        """
        # build my value
        value = Raster(dataset=dataset)
        # and return it
        return value

    def _pyre_push(self, src, dest):
        """
        Push my cache value to disk
        """
        # get the src raster
        raster = src.value
        # build the work pile
        tiles = [raster.read()] + raster._staged
        # go through the assembled tiles
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
            dest._pyre_id.write(data=data, memtype=type, origin=origin, shape=shape)
        # all done
        return


# end of file
