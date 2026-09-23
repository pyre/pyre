# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved

# support
import journal
from .. import libh5

# the local exceptions
from . import exceptions

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
        # what the library had to say the last time an open failed
        self._pyre_reason = ""
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
        fapl: typing.Optional[libh5.properties.fapl],
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
            fapl = libh5.properties.fapl()
        # attach the required {ros3} driver information
        fapl.ros3(
            region=region,
            id=id,
            key=secret,
            token=token,
            authenticate=authenticate,
        )
        # delegate to the opener, which hands the driver the address it understands
        self._pyre_open(uri=s3, mode="r", fapl=fapl, **kwds)
        # but remember the uri the caller wrote, since that is the one they can act on
        # when something goes wrong; the rewritten https address names a bucket endpoint
        # nobody typed and would send them looking in the wrong place
        self._pyre_uri = uri
        # all done
        return self

    # diagnostics
    def _pyre_live(self) -> bool:
        """
        Check whether i am attached to a file the library is willing to talk about
        """
        # get my handle
        h5id = self._pyre_id
        # one i never made, or one i have since closed, is not a file
        if h5id is None:
            # so say so
            return False
        # otherwise, the library is the authority on whether the handle is still good
        return libh5.valid(h5id.hid)

    def _pyre_diagnose(self, path: typing.Optional[pyre.primitives.pathlike] = None) -> Exception:
        """
        Explain why i have nothing to offer at {path}

        An open that fails leaves me holding an empty handle rather than raising, and the
        library reports its reasons on an error stack of its own that the caller never
        sees. So whoever finds nothing here has to work out which of two things happened,
        and this is where that is decided: either i never opened, or i am open and simply
        hold nothing at the path that was asked for
        """
        # a handle the library will not vouch for means the open is what failed: a product
        # that is missing or unreadable, one that is not h5 at all, or, for a product in a
        # bucket, credentials that are wrong or no longer current
        if not self._pyre_live():
            # so name the file rather than the path, and pass along what the library said
            return exceptions.OpenError(uri=self._pyre_uri, reason=self._pyre_reason)
        # otherwise i am attached to a real file that holds nothing there
        return exceptions.PathError(uri=self._pyre_uri, path=path)

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
        fcpl: typing.Optional[libh5.properties.fcpl] = None,
        fapl: typing.Optional[libh5.properties.fapl] = None,
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
            fcpl = libh5.properties.fcpl.default
        # similarly, if the supplied {fapl} is trivial
        if fapl is None:
            # get the default
            fapl = libh5.properties.fapl.default
        # open the file
        self._pyre_id = libh5.File(uri=str(uri), fcpl=fcpl, fapl=fapl, **kwds)
        # if the library refused, its reasons sit on its error stack only until the next call
        # into it, and asking whether the handle is live is such a call; so collect them first
        reason = libh5.explanation()
        # and keep them only if the open is what failed
        self._pyre_reason = "" if self._pyre_live() else reason
        # all done
        return self


# end of file
