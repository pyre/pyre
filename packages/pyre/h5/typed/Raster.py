# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import journal

# typing
import typing
from .. import libh5


# the value of an array dataset
class Raster:
    """
    The value of a dataset that holds a non-trivial array

    Rasters are cheap handles: building one moves no data. Nothing about a non-trivial
    dataset determines how its consumer intends to touch it, so the raster does not commit
    to an access strategy; instead, it carries the hdf5 metadata that informs the choice,
    and the factories that realize it: {tile} materializes a dense private grid on the heap,
    while {mosaic} builds an out-of-core view whose chunks move only when asked to
    """

    # metadata: the decision-driving questions
    @property
    def dataset(self):
        """
        Get the handle to my dataset
        """
        # reach through my node for the h5 object; anything not answered by my named
        # properties can be asked of the handle directly
        return self._dataset._pyre_id

    @property
    def schema(self):
        """
        Get my layout
        """
        # reach through my node
        return self._dataset._pyre_layout

    @property
    def shape(self) -> typing.List[int]:
        """
        Get my extent along each axis
        """
        # my node knows
        return self._dataset.shape

    @property
    def rank(self) -> int:
        """
        Get my number of axes
        """
        # measure my shape
        return len(self.shape)

    @property
    def memtype(self):
        """
        Get my in-memory type
        """
        # my layout knows
        return self._dataset._pyre_layout.memtype

    @property
    def disktype(self):
        """
        Get my on-disk type
        """
        # my node knows the actual type of the dataset in the file
        return self._dataset.type

    @property
    def layout(self):
        """
        Get the storage layout of my on-disk representation
        """
        # ask my creation property list
        return self.dcpl.layout

    @property
    def chunk(self) -> typing.Optional[typing.List[int]]:
        """
        Get my chunk shape, or {None} if my on-disk representation is not chunked
        """
        # my node knows; storage that is not chunked reports no shape at all
        chunk = self._dataset.chunk
        # turn that into something a client can test against
        return chunk if chunk else None

    @property
    def filters(self):
        """
        Get the filter pipeline of my on-disk representation
        """
        # my node knows
        return self._dataset.filters

    # metadata: the property lists, for everything not promoted to a named property
    @property
    def dcpl(self):
        """
        Get the creation property list of my dataset
        """
        # my node knows
        return self._dataset.dcpl

    @property
    def dapl(self):
        """
        Get the access property list of my dataset
        """
        # my node knows
        return self._dataset.dapl

    # the access strategy factories
    def tile(
        self,
        *,
        origin: typing.Optional[typing.Sequence[int]] = None,
        shape: typing.Optional[typing.Sequence[int]] = None,
    ):
        """
        Allocate a dense grid on the heap over the window at {origin} with the given {shape}
        and fill it with my data

        The grid is a private copy: writes to it do not flow back to the file; its indices
        are tile-local, and the caller is responsible for remembering {origin}
        """
        # normalize the origin
        if origin is None:
            # to the beginning of my extent
            origin = [0] * self.rank
        # normalize the shape
        if shape is None:
            # to the remainder of my extent past {origin}
            shape = [extent - base for extent, base in zip(self.shape, origin)]
        # get my in-memory type
        memtype = self.memtype
        # ask it for a heap grid big enough to hold the window
        data = memtype.grid(shape=shape)
        # if the allocation failed because there is no grid support for my cell type
        if data is None:
            # bail; the {memtype} has already complained
            return None
        # populate the grid with my content
        self.dataset.read(data=data, memtype=memtype.htype, origin=origin, shape=shape)
        # and hand it off
        return data

    def mosaic(
        self,
        *,
        origin: typing.Optional[typing.Sequence[int]] = None,
        shape: typing.Optional[typing.Sequence[int]] = None,
    ):
        """
        Build an out-of-core view of my data over the window at {origin} with the given
        {shape}; when no window is specified, the view covers my full extent

        Nothing is resident until a chunk is filled: chunked datasets are diced into their
        own chunks, contiguous ones are a single tile
        """
        # the name of my cell type in the grid vocabulary
        cell = self.memtype.cell
        # if my cell type has no grid support
        if cell is None:
            # make a channel
            channel = journal.error("pyre.h5.typed")
            # complain
            channel.line(f"no grid support for the '{self.memtype.tag}' cell type")
            channel.line(f"while building a mosaic over '{self._dataset._pyre_location}'")
            # flush
            channel.log()
            # and bail, just in case errors aren't fatal
            return None
        # with no window specified
        if origin is None and shape is None:
            # the mosaic covers my full extent over the dataset's own tiling
            return self.dataset.mosaic(cell=cell)
        # otherwise, normalize the origin
        if origin is None:
            # to the beginning of my extent
            origin = [0] * self.rank
        # and the shape
        if shape is None:
            # to the remainder of my extent past {origin}
            shape = [extent - base for extent, base in zip(self.shape, origin)]
        # build the smallest mosaic that covers the window
        return self.dataset.mosaic(cell=cell, base=origin, shape=shape)

    # metamethods
    def __init__(self, dataset, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my dataset node; the reference is deliberately strong: i am the object the
        # user walks away with, so i must keep my node, and through it the file, alive
        self._dataset = dataset
        # all done
        return

    def __str__(self):
        # render my extents the way {h5ls} does
        extents = ", ".join(map(str, self.shape))
        # name my cell type, falling back to the memtype tag when the grid vocabulary
        # has no entry for it
        cell = self.memtype.cell or self.memtype.tag
        # get my storage layout
        layout = self.layout
        # if my storage is chunked
        if layout == libh5.Layout.chunked:
            # describe the tiling
            storage = "chunked {" + ", ".join(map(str, self.chunk)) + "}"
        # otherwise
        else:
            # the layout name says it all
            storage = layout.name
        # render
        return f"raster '{self._dataset._pyre_location}' {{{extents}}} of {cell}, {storage}"


# end of file
