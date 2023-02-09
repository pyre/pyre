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
        query: typing.Optional[schema.group] = None,
        at: pyre.primitives.pathlike = "/",
        **kwds,
    ) -> typing.Optional[Object]:
        """
        Read {file} and extract an h5 {object} with the structure of {query}
        """
        # analyze the {uri} and build the h5 {file}, passing any extra arguments to it
        file = self.open(uri=uri, mode=mode, **kwds)
        return file
        # set the anchor at the requested location in the file
        anchor = file._pyre_find(path=pyre.primitives.path(path))
        return anchor
        # normalize the desired layout
        if query is None:
            # get my schema
            query = self.schema(file=file)
        # visit the {query} and populate the {file}
        query._pyre_identify(authority=self, parent=file)
        # find where {query} fits within {file} and return it
        return file

    # implementation details
    def open(self, uri: pyre.primitives.uri, mode, **kwds) -> typing.Optional[File]:
        """
        Open an h5 file object
        """
        # parse the {uri}, using {file} as the default scheme
        uri = pyre.primitives.uri.parse(value=uri, scheme="file")
        # and extract the {scheme}
        scheme = uri.scheme
        # if the {scheme} points to a local {file}
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
        channel.line(f"unknown scheme '{scheme}'")
        # flush
        channel.log()
        # and bail, in case errors aren't fatal
        return

    def schema(self, file, **kwds) -> schema.group:
        """
        Retrieve the schema of the data product
        """
        # the default is dynamic discovery, implemented by getting an explorer
        explorer = Explorer()
        # to discover the structure of the file
        return explorer.visit(file=file)


# end of file
