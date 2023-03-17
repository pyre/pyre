# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# external
import pyre

# superclass
from .Identifier import Identifier

# typing
import typing


# base class of all h5 objects that have an address
class Location(Identifier):
    """
    The base class for all h5 objects that have an address
    """

    # metamethods
    def __init__(self, at: typing.Optional[pyre.primitives.pathlike] = None, **kwds):
        # chain up
        super().__init__(**kwds)
        # record the location
        self._pyre_location = pyre.primitives.path(at) if at is not None else None
        # all done
        return

    # framework hooks
    # access to contents by category; all trivial by default
    def _pyre_datasets(self) -> typing.Sequence[str]:
        """
        Generate a sequence of my datasets
        """
        # nothing from me
        return []

    def _pyre_groups(self) -> typing.Sequence[str]:
        """
        Generate a sequence of my subgroups
        """
        # nothing from me
        return []

    def _pyre_locations(self) -> typing.Sequence[str]:
        """
        Generate a sequence of contents
        """
        # nothing from me
        return []

    # visiting
    def _pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a location
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority._pyre_onLocation
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super()._pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(location=self, **kwds)


# end of file
