# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# external
import journal
import pyre

# support
from .Assembler import Assembler

# typing
import typing
from .. import schema
from .Object import Object
from .Dataset import Dataset
from .Group import Group
from .File import File

# alias the h5 bindings
from .. import libh5

# the exception raised by an unresolved shape dimension
from pyre.calc.exceptions import UnresolvedNodeError


# the writer
class Writer:
    """
    The base writer of h5 data products

    This is a visitor that persists the contents of an in-memory object to an HDF5 file.
    Datasets are sized from their resolved shape dimensions; an optional member whose
    dimensions are unresolved is treated as absent, so the set of dimensions a realization
    supplies controls both the extents and the presence of its contents.
    """

    # interface
    def write(
        self,
        data: typing.Optional[Object] = None,
        query: typing.Optional[schema.descriptor] = None,
        **kwds,
    ) -> None:
        """
        Persist an h5 {data} product; the optional {query} argument is a {schema} that constrains
        the traversal and provides complete control over what gets written to the file
        """
        # make sure there is something to write
        if data is None and query is None:
            # if not, there is nothing to do
            return None
        # if i don't have {data}
        if data is None:
            # i must have structure, so build an empty data object
            assembler = Assembler()
            # using the structure we are traversing
            data = assembler.visit(descriptor=query)
        # the shape index, if my layout is a product root; {None} for a plain group
        shapes = getattr(data._pyre_layout, "_pyre_shapes", None)
        # the destination handle; assume i am attached to a valid {file}
        dst = self._file._pyre_id
        # the product mounts at the root's location; create the prefix groups above it
        location = data._pyre_location
        for part in location.parent.names:
            # reusing an existing group or creating a new one
            dst = dst.get(path=part) if part in dst else dst.create(path=part)
        # the depth of the mount, so dataset locations can be made schema-relative
        depth = len(list(location.names))
        # traverse the structure and persist the content
        data._pyre_identify(authority=self, dst=dst, shapes=shapes, depth=depth, **kwds)
        # all done
        return

    # metamethods
    def __init__(
        self,
        uri: pyre.primitives.uri,
        mode: str = "w",
        fcpl: typing.Optional[libh5.properties.fcpl] = None,
        **kwds,
    ):
        # chain up
        super().__init__(**kwds)
        # build the file object
        self._file = self._pyre_open(uri=uri, mode=mode, fcpl=fcpl)
        # all done
        return

    # framework hooks
    def _pyre_onGroup(self, group: Group, dst: libh5.Group, shapes, depth, **kwds) -> None:
        """
        Process a {group}
        """
        # an optional group whose provided dimensions are unresolved is absent
        if group._pyre_layout._pyre_optional and not self._pyre_present(
            group=group, shapes=shapes, depth=depth
        ):
            # so skip it
            return
        # form the name of the target group in the output
        name = group._pyre_location.name
        # reuse it if present, otherwise make it
        hid = dst.get(path=name) if name in dst else dst.create(path=name)
        # now, go through the group contents
        for member in group._pyre_locations():
            # and ask each member to identify itself
            member._pyre_identify(
                authority=self, dst=hid, shapes=shapes, depth=depth, **kwds
            )
        # all done
        return

    def _pyre_onDataset(
        self, dataset: Dataset, dst: libh5.Group, shapes, depth, **kwds
    ) -> None:
        """
        Process a dataset
        """
        # get its layout and declared shape, if any
        layout = dataset._pyre_layout
        shape = getattr(layout, "shape", None)
        # a dataset that names dimensions, in a tree with a shape index, is sized from the
        # resolved dimensions
        if shapes is not None and shape and any(isinstance(a, str) for a in shape):
            # so realize it from its resolved shape
            self._pyre_writeArray(
                dataset=dataset, layout=layout, shape=shape, dst=dst, shapes=shapes, depth=depth
            )
            # all done
            return
        # otherwise it is a scalar, a dynamic container, or a value-shaped array; write it only
        # if the user has supplied a value
        if dataset._value is not None:
            # describe and persist it
            self._pyre_writeValue(dataset=dataset, dst=dst)
        # all done
        return

    # implementation details
    def _pyre_writeArray(self, dataset, layout, shape, dst, shapes, depth) -> None:
        """
        Create an array dataset sized from its resolved shape dimensions and persist it
        """
        # the dataset's schema-relative path
        relpath = self._pyre_relpath(location=dataset._pyre_location, depth=depth)
        # attempt to resolve every axis into a concrete extent
        try:
            # an int is fixed, an Ellipsis is free, a name resolves through the index
            extents = [self._pyre_extent(axis, relpath, shapes) for axis in shape]
        # if a named dimension has no value
        except UnresolvedNodeError:
            # an optional dataset with unset dimensions is simply absent
            if layout._pyre_optional:
                # so skip it
                return
            # a required dataset that cannot be sized is a bug in the realization
            channel = journal.firewall("pyre.h5.api.writer")
            # describe it
            channel.line(f"cannot size the required dataset '{relpath}'")
            channel.line(f"one of its shape dimensions is unresolved")
            # flush
            channel.log()
            # in case firewalls are not fatal, abandon this dataset
            return
        # the name in the parent
        name = dataset._pyre_location.name
        # if it already exists, reuse it
        if name in dst:
            # look it up
            hid = dst.get(path=name)
        # otherwise create it at the resolved extents, with the on-disk type
        else:
            # the dataspace
            space = libh5.DataSpace(shape=extents)
            # creation and access configuration
            dcpl = libh5.properties.dcpl()
            dapl = libh5.properties.dapl()
            # make the dataset
            hid = dst.create(
                path=name, type=layout.disktype, space=space, dcpl=dcpl, dapl=dapl
            )
        # if the user supplied data, flush it; otherwise leave the dataset fill-valued
        if dataset._value is not None:
            # persist the bound value
            dataset._pyre_write(dst=hid)
        # all done
        return

    def _pyre_writeValue(self, dataset, dst) -> None:
        """
        Create a dataset from its value-derived description and persist it
        """
        # form the name
        name = dataset._pyre_location.name
        # if it already exists, reuse it
        if name in dst:
            # look it up
            hid = dst.get(path=name)
        # otherwise build it from the layout's description
        else:
            # ask the dataset for its type and shape
            datatype, dataspace, chunk, *_ = dataset._pyre_describe()
            # creation and access configuration
            dcpl = libh5.properties.dcpl()
            dapl = libh5.properties.dapl()
            # honor the chunking strategy, if any
            if chunk:
                # by configuring the creation property list
                dcpl.setChunk(chunk)
            # make the dataset
            hid = dst.create(
                path=name, type=datatype, space=dataspace, dcpl=dcpl, dapl=dapl
            )
        # persist the value
        dataset._pyre_write(dst=hid)
        # all done
        return

    def _pyre_present(self, group, shapes, depth) -> bool:
        """
        Whether all the dimensions {group} provides are resolved
        """
        # if there is no shape index, presence is not governed by dimensions
        if shapes is None:
            # so the group is present
            return True
        # the group's schema-relative path
        relpath = self._pyre_relpath(location=group._pyre_location, depth=depth)
        # go through the dimensions this group provides
        for dimension in group._pyre_layout._pyre_dimensions():
            # build the key
            name = dimension._pyre_name
            key = f"{relpath}.{name}" if relpath else name
            # attempt to read the node
            try:
                # if it is unresolved, this raises
                shapes.retrieve(key).value
            # an unresolved dimension means the group is absent this realization
            except UnresolvedNodeError:
                # so report it absent
                return False
        # all dimensions resolved; the group is present
        return True

    def _pyre_extent(self, axis, relpath, shapes):
        """
        Resolve a single {shape} axis into a concrete extent
        """
        # an int is a fixed extent
        if isinstance(axis, int):
            # use it as is
            return axis
        # an Ellipsis is a free extent
        if axis is Ellipsis:
            # which we render as zero, for now
            return 0
        # otherwise it names a dimension, resolved through the index by the alias the
        # resolver registered at my path; reading an unset one raises {UnresolvedNodeError}
        return shapes.retrieve(f"{relpath}.{axis}").value

    @staticmethod
    def _pyre_relpath(location, depth):
        """
        Render {location} relative to the mount as a dotted, schema-relative path
        """
        # drop the mount prefix and join with dots
        return ".".join(list(location.names)[depth:])

    def _pyre_open(
        self, uri: pyre.primitives.urilike, mode: str, **kwds
    ) -> typing.Optional[File]:
        """
        Open an h5 file object
        """
        # parse the {uri}, using {file} as the default scheme
        uri = pyre.primitives.uri.parse(value=uri, scheme="file")
        # and extract the {scheme}
        scheme = uri.scheme
        # if the {scheme} points to a local path
        if scheme == "file":
            # make a local {file} object whose path is the {address} of the {uri} and return it
            return File()._pyre_local(uri=uri.address, mode=mode, **kwds)
        # if we get this far, the {uri} was malformed; make a channel
        channel = journal.error("pyre.h5.reader")
        # complain
        channel.line(f"could not open an h5 file")
        channel.line(f"with the given uri '{uri}':")
        channel.line(f"the scheme '{scheme}' is not supported")
        # flush
        channel.log()
        # and bail, in case errors aren't fatal
        return


# end of file
