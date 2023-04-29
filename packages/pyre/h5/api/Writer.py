# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# external
import journal
import pyre

# support
from .Explorer import Explorer

# typing
import typing
from .. import schema
from .Object import Object
from .Dataset import Dataset
from .Group import Group
from .File import File


# the writer
class Writer:
    """
    The base writer of h5 data products

    This is a visitor that populates an h5 file from the contents of a in memory object given
    a {query} that describes a subset of the data hierarchy
    """

    # interface
    def write(
        self,
        data: Object,
        uri: pyre.primitives.uri,
        mode: str = "w",
        path: pyre.primitives.pathlike = "/",
        query: typing.Optional[schema.descriptor] = None,
        errors: typing.Optional[typing.Sequence[Object]] = None,
        **kwds,
    ) -> typing.Optional[File]:
        """
        Open {uri} and save an h5 {data} product with the structure of {query}
        """
        # analyze the {uri} and build the h5 {file}, passing any extra arguments to it
        file = self.open(uri=uri, mode=mode, **kwds)
        # if anything went wrong
        if file is None:
            # assume that the error has already been reported and bail, just in case errors
            # aren't fatal
            return None
        # normalize the desired layout
        if query is None:
            # get my schema
            query = data._pyre_layout
        # normalize the starting path
        path = pyre.primitives.path(path)
        # look up the h5 location that serves as the query anchor
        parent = file._pyre_find(path=path)
        # traverse the structure and build the content
        return query._pyre_identify(
            authority=self,
            name=path.name,
            parent=parent,
            data=data,
            file=file,
            errors=errors,
        )

    # framework hooks
    def _pyre_onDataset(
        self,
        dataset: schema.dataset,
        file: File,
        name: str,
        parent: Group,
        data: typing.Optional[Dataset],
        errors,
        **kwds,
    ) -> Group:
        """
        Process a dataset
        """
        # there are three sources of truth regarding the dataset at hand:
        #   {dataset}: with the static layout of the parent group
        #   {data}:    the object we are saving in the new {file}, which may not exist
        #   {parent}:  whatever may be stored in the file already
        # there are two pieces of information that must be checked for consistency:
        #   the dataset type
        #   the dataset shape
        #
        # attempt to
        try:
            # look up {name} within {parent}
            entry = parent._pyre_find(path=name)
        # if it's not there
        except RuntimeError:
            # compute its location relative to its parent
            location = parent._pyre_location / name
            # its space should be identical to its source
            space = data._pyre_id.space
            # for the type, prefer the potentially more accurate type from the spec, if it's there
            # and fall back to whatever is known about the source type
            # type = (
            # dataset.disktype if dataset.disktype is not None else data._pyre_id.type
            # )
            type = data._pyre_id.type
            # build the low level object
            hid = parent._pyre_id.create(path=name, type=type, space=space)
            # realize it
            entry = Dataset(id=hid, at=location, layout=dataset)
        # if it is already there
        else:
            # compare the types/shapes and check for whatever consistency guarantees are
            # necessary for the data copy to follow
            pass
        # we have structure; make content
        entry._pyre_write(file=file, src=data)
        # all done
        return parent

    def _pyre_onGroup(
        self,
        group: schema.group,
        file: File,
        name: str,
        parent: Group,
        data: typing.Optional[Group],
        errors,
        **kwds,
    ) -> Group:
        """
        Process a {group}
        """
        # attempt to
        try:
            # look up this {name} within {parent}
            entry = parent._pyre_find(path=name)
        # if anything goes wrong
        except RuntimeError:
            # no worries; build the group
            entry = Group(
                id=parent._pyre_id.create(path=name),
                at=parent._pyre_location / name,
                layout=group,
            )
        # if it's there
        else:
            # and we've stumbled into something that's not a group
            if not isinstance(entry, Group):
                # we have a problem; make a channel
                channel = journal.error("pyre.h5.reader")
                # make a report
                channel.line(f"type mismatch in '{parent._pyre_location / name}'")
                channel.line(f"expected a group, got {entry}")
                channel.line(f"while writing '{file}'")
                # flush
                channel.log()
                # and bail, just in case errors aren't fatal
                return parent
        # now, go through the group contents
        for descriptor in group._pyre_descriptors():
            # get the descriptor name
            name = descriptor._pyre_name
            # if we have {data}
            if data:
                # and it knows {name}
                try:
                    # get the associated object
                    object = data._pyre_find(path=name)
                # if it doesn't
                except RuntimeError:
                    # no worries, just build structure
                    object = None
            # if not
            else:
                # no worries, just build structure
                object = None
            # identify the descriptor
            descriptor._pyre_identify(
                authority=self,
                name=name,
                parent=entry,
                file=file,
                data=object,
                errors=errors,
            )
        # all done
        return parent

    # implementation details
    def open(
        self, uri: typing.Union[pyre.primitives.uri, str], mode: str, **kwds
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
