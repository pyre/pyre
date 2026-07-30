# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import journal

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
        Build my value: an out-of-core mosaic wired to {dataset}
        """
        # the name of my cell type in the grid vocabulary
        cell = self.memtype.cell
        # if my cell type has no grid support
        if cell is None:
            # make a channel
            channel = journal.error("pyre.h5.typed")
            # complain
            channel.line(f"no grid support for the '{self.memtype.tag}' cell type")
            channel.line(f"while pulling the value of '{dataset._pyre_location}'")
            # flush
            channel.log()
            # and bail, just in case errors aren't fatal
            return None
        # ask the dataset for a mosaic over its own storage layout: chunked products are
        # diced into their chunks, contiguous ones are a single tile; nothing is resident
        # until the consumer fills the tiles it needs
        return dataset._pyre_id.mosaic(cell=cell)

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
        # my values are mosaics wired to their own backing store: push whatever diverged;
        # this covers updating a product in place; carrying content to a {dst} in another
        # file is value binding, an open part of the writer design
        value.flush()
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
