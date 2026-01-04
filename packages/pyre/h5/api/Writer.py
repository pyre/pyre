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


# the writer
class Writer:
    """
    The base writer of h5 data products

    This is a visitor that persists the contents of an in-memory object to an HDF5 file.
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
        # the traversal requires structure,
        if query is None:
            # so if the user didn't provide a map, borrow from the data object
            query = data._pyre_layout
        # get the destination handle; assume i am attached to valid {file}
        dst = self._file._pyre_id
        # traverse the structure and persist the content
        data._pyre_identify(authority=self, dst=dst, **kwds)
        # all done
        return

    # metamethods
    def __init__(
        self,
        uri: pyre.primitives.uri,
        mode: str = "w",
        fcpl: typing.Optional[libh5.FCPL] = None,
        **kwds,
    ):
        # chain up
        super().__init__(**kwds)
        # build the file object
        self._file = self._pyre_open(uri=uri, mode=mode, fcpl=fcpl)
        # all done
        return

    # framework hooks
    def _pyre_onDataset(self, dataset: Dataset, dst: libh5.Group, **kwds) -> None:
        """
        Process a dataset
        """
        # form the {dataset} name as known by its parent
        name = dataset._pyre_location.name
        # if {name} is already present in {dst}
        if name in dst:
            # look up the {dataset} in the output file
            hid = dst.get(path=name)
        # if it doesn't exist
        else:
            # we have to make it; ask the {dataset} for its type and shape
            datatype, dataspace, chunk, *_ = dataset._pyre_describe()
            # creation configuration
            dcpl = libh5.DCPL()
            # and access configuration
            dapl = libh5.DAPL()
            # if the chunking strategy is non-trivial
            if chunk:
                # configure the dataset creation
                dcpl.setChunk(chunk)
                # MGA: what to do with the dapl chunk cache values?
            # create the dataset
            hid = dst.create(
                path=name, type=datatype, space=dataspace, dcpl=dcpl, dapl=dapl
            )
        # we have structure; make content
        dataset._pyre_write(dst=hid)
        # all done
        return

    def _pyre_onGroup(self, group: Group, dst: libh5.Group, **kwds) -> None:
        """
        Process a {group}
        """
        # form the name of the target group in the output
        name = group._pyre_location.name
        # if {name} is already a member of {dst}
        if name in dst:
            # look it up
            hid = dst.get(path=name)
        # if it doesn't exist
        else:
            # make it
            hid = dst.create(path=name)
        # now, go through the group contents
        for member in group._pyre_locations():
            # and ask each member to identify itself
            member._pyre_identify(authority=self, dst=hid, **kwds)
        # all done
        return

    # implementation details
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
