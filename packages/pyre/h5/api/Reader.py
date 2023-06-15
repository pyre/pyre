# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# external
import journal
import pyre

# support
from .. import libh5
from .File import File
from .Explorer import Explorer

# typing
import typing
from .. import schema
from .Object import Object
from .Dataset import Dataset
from .Group import Group
from .Inspector import Inspector

# type aliases
ErrorReport = typing.List[Exception]


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
        path: pyre.primitives.pathlike = "/",
        query: typing.Optional[schema.descriptor] = None,
        **kwds,
    ) -> typing.Optional[Object]:
        """
        Open {uri} and extract an h5 {object} with the structure of {query} anchored at {path}
        """
        # get my file
        file = self._file
        # ask the file for its inspector
        inspector = file._pyre_inspector
        # normalize the target path
        path = pyre.primitives.path(path)
        # find the container group
        anchor = file._pyre_id.get(path=str(path))
        # and ask the inspector to infer the layout
        return inspector._pyre_inspect(h5id=anchor, path=path, query=query)

    # metamethods
    def __init__(
        self,
        uri: pyre.primitives.uri,
        mode: str = "r",
        fapl: typing.Optional[libh5.FAPL] = None,
        **kwds,
    ):
        # chain up
        super().__init__(**kwds)
        # build the file object
        self._file = self._pyre_open(uri=uri, mode=mode, fapl=fapl)
        # all done
        return

    # implementation details
    def _pyre_open(
        self,
        uri: typing.Union[pyre.primitives.uri, str],
        mode: str = "r",
        fapl: typing.Optional[libh5.FAPL] = None,
        **kwds,
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
            return File()._pyre_local(uri=uri.address, mode=mode, fapl=fapl, **kwds)
        # if the {scheme} points to an {s3} bucket
        if scheme == "s3":
            # check whether the installed {h5} library supports {ros3}
            if not libh5.ros3():
                # make a channel
                channel = journal.error("pyre.h5.reader")
                # complain
                channel.line(f"this installation of libhdf5 has no ros3 support")
                channel.line(f"while opening '{uri}'")
                # flush
                channel.log()
                # and bail
                return None
            # the supported uris are of the form
            #
            #   s3://profile@region/bucket/key
            #
            # parse the authority field
            region, _, profile, _ = uri.server
            # parse the path to the file
            _, bucket, *key = pyre.primitives.path(uri.address)
            # open the remote file and return it
            return File()._pyre_ros3(
                fapl=fapl,
                region=region,
                profile=profile,
                bucket=bucket,
                key="/".join(key),
            )

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
