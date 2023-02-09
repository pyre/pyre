# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved

# support
import journal

# superclass
from .Group import Group

# typing
import pyre
import typing
from .Object import Object


# file is a group at '/'
class File(Group):
    """
    A container at the root of a hierarchy
    """

    # metamethods
    def __init__(self, at: pyre.primitives.pathlike = "/", **kwds):
        # chain up
        super().__init__(at=at)
        # initialize my access property list
        self._pyre_fapl = None
        # initially, i'm not attached to a particular file
        self._pyre_uri = None
        # all done
        return

    def __del__(self):
        # get my access parameter list
        fapl = self._pyre_fapl
        # if it is non-trivial
        if fapl is not None:
            # close it
            fapl.close()
            # and discard it
            self._pyre_fapl = None
        # chain up
        super().__del__()
        # all done
        return

    # representation
    def __str__(self):
        """
        Build a human readable representation
        """
        # easy enough
        return f"file '{self._pyre_uri}'"

    # framework hooks
    # attach to local files
    def _pyre_local(
        self, uri: pyre.primitives.pathlike, mode: str = "r", **kwds
    ) -> "File":
        """
        Access the local h5 file at {uri}

        The parameter {mode} can be one of:

            r: read only
           r+: read/write, file must exist
            w: create file, truncate if it exists
           w-: create file, fail if it exists
            x: alias for w-
        """
        # delegate to the opener
        return self._pyre_open(uri=uri, mode=mode, **kwds)

    # attach to S3 buckets
    def _pyre_ros3(
        self, bucket: str, key: str, profile: typing.Optional[str] = None
    ) -> "File":
        """
        Access the remote dataset {key} in the given S3 {bucket} using the {ROS3} driver
        """
        # grab the h5 bindings
        h5 = pyre.libh5
        # if the library doesn't have support for {ros3}
        if not h5.ros3():
            # make a channel
            channel = journal.error("pyre.h5.file.ros3")
            # complain
            channel.line("this installation of libhdf5 has no support for ros3")
            channel.line(f"while looking for key '{key}' in bucket '{bucket}'")
            # flush
            channel.log()
            # and bail, just in case errors aren't fatal
            return self

        # make an access parameter list and fill it with {ros3} information
        fapl = h5.FAPL().ros3()
        # assemble the file uri
        uri = f"https://{bucket}.s3.amazonaws.com{key}"
        # and delegate to the opener
        return self._pyre_open(uri=uri, mode="r", fapl=fapl)

    # clean up
    def _pyre_close(self):
        """
        Detach me from all h5 resources
        """
        # get my access parameter list
        fapl = self._pyre_fapl
        # if it's non-trivial
        if fapl is not None:
            # close it
            fapl.close()
            # and clear my state
            self._pyre_fapl = None
        # and chain up
        return super()._pyre_close()

    # structural
    def _pyre_root(self) -> Group._pyre_schema.group:
        """
        Get the root of my layout
        """
        # get my layout
        layout = self._pyre_layout
        # if it is trivial
        if layout is None:
            # build an empty group at the root
            layout = self._pyre_schema.group(name="root")
        # either way
        return layout

    # member access
    def _pyre_find(self, path: pyre.primitives.pathlike) -> typing.Optional[Object]:
        """
        Look up the h5 {object} associated with {path}
        """
        # normalize the input {path}
        path = pyre.primitives.path(path)
        # if the request is for the root object
        if path == pyre.primitives.path.root:
            # return me
            return self
        # otherwise, delegate to the {group} that i am to look up my members
        return super()._pyre_find(path=path)

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a file
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onFile
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(file=self, **kwds)

    # helpers
    def _pyre_open(self, uri: pyre.primitives.pathlike, mode: str, fapl=None) -> "File":
        """
        Access to the h5 file factory

        This is a lower level interface that does no error checking;
        it's probably not what you are looking for
        """
        # grab the h5 bindings
        h5 = pyre.libh5
        # record the uri
        self._pyre_uri = uri
        # and the access property list
        self._pyre_fapl = fapl
        # open the file
        self._pyre_id = (
            h5.File(uri=str(uri), mode=mode)
            if fapl is None
            else h5.File(uri=str(uri), mode=mode, fapl=fapl)
        )
        # all done
        return self


# end of file
