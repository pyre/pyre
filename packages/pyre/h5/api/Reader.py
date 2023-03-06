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


# the reader
class Reader:
    """
    The base reader of h5 data products

    This is a visitor that populates an h5 object from the contents of a file given a {query}
    that describes a subset of the hierarchy
    """

    # interface
    def read(
        self,
        uri: pyre.primitives.uri,
        mode: str = "r",
        path: pyre.primitives.pathlike = "/",
        query: typing.Optional[schema.descriptor] = None,
        errors: typing.Optional[typing.Sequence[Object]] = None,
        **kwds,
    ) -> typing.Optional[Object]:
        """
        Open {uri} and extract an h5 {object} with the structure of {query} anchored at {path}
        """
        # analyze the {uri} and build the h5 {file}, passing any extra arguments to it
        file = self.open(uri=uri, mode=mode, **kwds)
        # if anything went wrong
        if file is None:
            # assume that the error has already been reported and bail
            return None
        # normalize the desired layout
        if query is None:
            # get my schema
            query = self._pyre_schema(file=file)
        # look up the h5 location that serves as the query anchor
        anchor = file._pyre_find(path=path)
        # visit the {query} and return the resulting h5 location
        return query._pyre_identify(
            authority=self, file=file, object=anchor, errors=errors
        )

    # framework hooks
    def _pyre_onGroup(
        self, file: File, object: Group, group: schema.group, errors
    ) -> Group:
        """
        Process a {group}
        """
        # getting here implies that the lookup of the {object} that corresponds
        # to the {group} layout was successful; the lookup endows {object} with
        # its {_pyre_id} and {_pyre_location}; it also builds a {_pyre_layout},
        # but it's not as articulated as {group} is, so we replace it; finally,
        # the {_pyre_descriptors} and values of the {object} attributes must be
        # populated
        #
        # get the {object} layout
        layout = object._pyre_layout
        # if the {object} has deduced its layout already and it is not a group
        if layout is not None and not isinstance(layout, schema.group):
            # there is a mismatch between the schema and the contents of the file
            # make a channel
            channel = journal.warning("pyre.h5.reader")
            # make a report
            channel.line(f"type mismatch in '{object._pyre_location}'")
            channel.line(f"expected a group, got {layout}")
            channel.line(f"while reading '{file._pyre_uri}'")
            # flush it
            channel.log()
            # add the {group} to the error pile
            if errors is not None:
                # if the caller cares
                errors.append(group)
            # and bail
            return object
        # replace the layout with the {group}
        object._pyre_layout = group
        # go through the group contents
        for descriptor in group._pyre_descriptors():
            # get its name
            name = descriptor._pyre_name
            # attempt to
            try:
                # look up the name
                entry = object._pyre_find(path=name)
            # if anything goes wrong
            except RuntimeError:
                # make a channel
                channel = journal.warning("pyre.h5.reader")
                # make a report
                channel.line(f"could not find '{name}'")
                channel.line(f"at {object._pyre_location}")
                channel.line(f"while reading '{file._pyre_uri}'")
                # flush it
                channel.log()
                # and ignore this descriptor
                continue
            # figure out what it is
            descriptor._pyre_identify(
                authority=self, file=file, object=entry, errors=errors
            )
            # attach the {entry} to {object} under {name}
            setattr(object, name, entry)
        # all done
        return object

    def _pyre_onDataset(
        self, file: File, object: Dataset, dataset: schema.dataset, errors
    ) -> Dataset:
        """
        Process a dataset
        """
        # get the {object} layout
        layout = object._pyre_layout
        # if it's non-trivial make sure it's compatible with its schema
        if layout is not None and not isinstance(layout, type(dataset)):
            # there is a mismatch between the schema and the contents of the file
            # make a channel
            channel = journal.warning("pyre.h5.reader")
            # make a report
            channel.line(f"type mismatch in {object._pyre_location}")
            channel.line(f"expected a {dataset}")
            channel.line(f"but got a {layout}")
            channel.line(f"while reading '{file._pyre_uri}'")
            # flush it
            channel.log()
            # add the {dataset} to the error pile
            if errors is not None:
                # if the caller cares
                errors.append(dataset)
            # and bail
            return object
        # read the dataset value
        object._pyre_read(file=file)
        # all done
        return object

    def _pyre_schema(self, file, **kwds) -> schema.group:
        """
        Retrieve the schema of the data product
        """
        # the default is dynamic discovery, implemented by getting an explorer
        explorer = Explorer()
        # to discover the structure of the file
        return explorer.visit(object=file)

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
        # if the {scheme} points to an {s3} bucket
        if scheme == "s3":
            # check whether the installed {h5} library supports {ros3}
            if not pyre.libh5.ros3():
                # make a channel
                channel = journal.error("pyre.h5.reader")
                # complain
                channel.line("this installation of libhdf5 has no support for ros3")
                channel.line(f"while looking for '{uri}'")
                # flush
                channel.log()
                # and bail
                return None
            # interpret the {authority} field as the {bucket} name
            authority = uri.authority
            # as such, it must be there; if not
            if authority is None:
                # make a channel
                channel = journal.error("pyre.h5.reader")
                # complain
                channel.line(f"couldn't figure out the S3 bucket name")
                channel.line(f"while parsing '{uri}':")
                channel.line(f"the 'authority' field is null")
                # flush
                channel.log()
                # and bail, in case errors aren't fatal
                return None
            # if it is there, take it apart
            fields = authority.split("@")
            # extract the authentication profile and the bucket name
            profile, bucket = fields if len(fields) == 2 else ("", authority)
            # get the object key
            key = uri.address
            # open the remote file and return it
            return File()._pyre_ros3(profile=profile, bucket=bucket, key=key)
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
