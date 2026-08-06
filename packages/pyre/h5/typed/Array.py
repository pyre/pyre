# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import journal

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
        # an unbound array has no value: content arrives either from a producer or from a
        # file, as an out-of-core mosaic built by {_pyre_pull}
        if value is self._default:
            # so there is nothing to build
            return None
        # bound content passes through untouched
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
        Build my value: a raster handle wired to {dataset}
        """
        # rasters are cheap: no metadata is copied and no data moves until the consumer
        # interrogates the handle and chooses an access strategy through its factories
        return Raster(dataset=dataset)

    def _pyre_push(self, src, dst: libh5.DataSet):
        """
        Push my cached value to disk
        """
        # get the value
        value = src.value
        # if nothing is bound
        if value is None:
            # there is nothing to push
            return
        # if the value is a raster
        if isinstance(value, Raster):
            # its content already lives in a file: data moves through the access objects
            # its factories build, and mosaics flush their own updates; carrying content
            # to a {dst} in another file is value binding, an open part of the writer design
            return
        # anything else is a foreign value; make a channel
        channel = journal.error("pyre.h5.typed")
        # complain
        channel.line(f"cannot push '{value}' to '{dst}'")
        channel.line(f"binding foreign values to array datasets is not supported yet")
        # flush
        channel.log()
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
