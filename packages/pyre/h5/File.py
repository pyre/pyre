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
    def open(self, path, mode):
        """
        Access the h5 file at {path}
        """
        # open the file and attach my handle
        self.pyre_id = pyre.libh5.File(path=str(path), mode=mode)
        # all done
        return self

    # metamethods
    def __init__(self, at="/", **kwds):
        # chain up with root as my location, unless the client has something else to suggest
        super().__init__(at=at, **kwds)
        # all done
        return

    # framework hooks
    def pyre_identify(self, authority: typing.Any, **kwds) -> typing.Any:
        """
        Let {authority} know i am a group
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
