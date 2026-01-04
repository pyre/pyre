# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

# support
import journal
from .. import libh5

# superclass
from .Group import Group

# typing
import pyre
import typing
from .. import schema
from .Object import Object


# file is a group at '/'
class File(Group):
    """
    A container at the root of a hierarchy
    """

    # metamethods
    def __init__(
        self,
        at: pyre.primitives.pathlike = "/",
        layout: typing.Optional[schema.group] = None,
        **kwds,
    ):
        # normalize the layout
        if layout is None:
            # by making sure it is a group
            layout = schema.group(name="root")
        # chain up
        super().__init__(at=at, layout=layout, **kwds)
        # initially, i'm not attached to a particular file
        self._pyre_uri = None
        # all done
        return

    # representation
    def __str__(self):
        """
        Build a human readable representation
        """
        # get my type info
        cls = type(self)
        name = cls.__name__
        module = cls.__module__
        # easy enough
        return f"file '{self._pyre_uri}', an instance of '{module}.{name}' "

    # framework hooks
    # attach to local files
    def _pyre_local(
        self,
        uri: pyre.primitives.pathlike,
        mode: str,
        **kwds,
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
        self,
        uri,
        credentials: dict,
        fapl: typing.Optional[libh5.FAPL],
        **kwds,
    ) -> "File":
        """
        Access the remote dataset {key} in the given S3 {bucket} using the {ROS3} driver
        """
        # unpack the {credentials}
        region = credentials["region"]
        id = credentials["access_key"]
        secret = credentials["secret_key"]
        token = credentials["token"]
        # get the bucket; it sits in the {authority} field, per AWS rules
        bucket = uri.authority
        # and the key, which is the {address} without the leading '/'
        key = str(uri.address)
        # form the {s3} uri
        s3 = f"https://{bucket}.s3.{region}.amazonaws.com{key}"
        # decide whether we are required to authenticate
        authenticate = id != "" and secret != ""
        # if the caller didn't supply a {fapl}
        if fapl is None:
            # set one up
            fapl = libh5.FAPL()
        # attach the required {ros3} driver information
        fapl.ros3(
            region=region,
            id=id,
            key=secret,
            token=token,
            authenticate=authenticate,
        )
        # and delegate to the opener
        return self._pyre_open(uri=s3, mode="r", fapl=fapl, **kwds)

    # structural
    def _pyre_root(self) -> schema.group:
        """
        Get the root of my layout
        """
        # get my layout; it's guaranteed to be a group with the correct name
        return self._pyre_layout

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
    def _pyre_open(
        self,
        uri: pyre.primitives.pathlike,
        fcpl: typing.Optional[libh5.FCPL] = None,
        fapl: typing.Optional[libh5.FAPL] = None,
        **kwds,
    ) -> "File":
        """
        Access to the h5 file factory

        This is a lower level interface that does no error checking;
        it's probably not what you are looking for
        """
        # record the uri
        self._pyre_uri = uri
        # if the supplied {fcpl} is trivial
        if fcpl is None:
            # get the default
            fcpl = libh5.FCPL.default
        # similarly, if the supplied {fapl} is trivial
        if fapl is None:
            # get the default
            fapl = libh5.FAPL.default
        # open the file
        self._pyre_id = libh5.File(uri=str(uri), fcpl=fcpl, fapl=fapl, **kwds)
        # all done
        return self


# end of file
