# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


# support
import pyre

# superclass
from .Group import Group

# typing
import typing


# a dataset container
class File(Group):
    """
    An h5 file
    """

    # interface
    def open(self, uri: pyre.primitives.pathlike, mode: str) -> "File":
        """
        Access the h5 file at {uri}

        The parameter {mode} can be one of:

            r: read only
           r+: read/write, file must exist
            w: create file, truncate if it exists
           w-: create file, fail if it exists
            x: alias for w-
        """
        # open the file and attach my handle
        self.pyre_id = pyre.libh5.File(path=str(uri), mode=mode)
        # all done
        return self

    def ros3(
        self, bucket: str, key: str, profile: typing.Optional[str] = None
    ) -> "File":
        """
        Access the remote dataset {key} in the given S3 {bucket}
        """
        # get the hdf5 bindings
        libh5 = pyre.libh5
        # if the library doesn't have support for {ros3}
        if not libh5.ros3():
            # make a channel
            channel = journal.error("pyre.h5.file")
            # complain
            channel.line("this installation of libhdf5 has no support for ros3")
            channel.line(f"while looking for key '{key}' in bucket '{bucket}'")
            # flush
            channel.log()
            # and bail
            return self
        # make a {ros3} access parameter list
        fapl = libh5.fapls.ros3(profile)
        # attach it
        self.pyre_fapl = fapl
        # open the file and attach my handle
        self.pyre_id = libh5.File(bucket, key, fapl)
        # all done
        return self

    # metamethods
    def __init__(self, at="/", fapl=None, **kwds):
        # chain up with root as my location, unless the client has something else to suggest
        super().__init__(at=at, **kwds)
        # record my access property list
        self.pyre_fapl = fapl
        # all done
        return

    # framework hooks
    def pyre_identify(self, authority: typing.Any, **kwds) -> typing.Any:
        """
        Let {authority} know i am a file
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority.pyre_onFile
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super().pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(group=self, **kwds)


# end of file
