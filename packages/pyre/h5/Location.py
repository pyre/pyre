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

    # access to contents by category; all trivial by default
    def pyre_datasets(self) -> typing.Sequence["Dataset"]:
        """
        Generate a sequence of my datasets
        """
        # nothing from me
        return []

    def pyre_groups(self) -> typing.Sequence["Group"]:
        """
        Generate a sequence of my subgroups
        """
        # nothing from me
        return []

    def pyre_locations(self) -> typing.Sequence["Location"]:
        """
        Generate a sequence of contents
        """
        # nothing from me
        return []

    # metamethods
    def __init__(
        self,
        name: typing.Optional[str] = None,
        at: typing.Optional[pyre.primitives.pathlike] = None,
        **kwds
    ):
        # chain up
        super().__init__(name=name, **kwds)
        # prefer {at} as the location, and fall back to {name} if it's trivial
        location = at or name
        # record the location
        self.pyre_location = pyre.primitives.path(location) if location else None
        # all done
        return

    # framework hooks
    def pyre_bind(self, name: str):
        """
        Attach my name
        """
        # chain up
        super().pyre_bind(name=name)
        # if i don't have a location
        if self.pyre_location is None:
            # use my name as my location
            self.pyre_location = pyre.primitives.path(name)
        # all done
        return

    def pyre_identify(self, authority, **kwds):
        """
        Let {authority} know i am a location
        """
        # attempt to
        try:
            # ask {authority} for my handler
            handler = authority.pyre_onLocation
        # if it doesn't understand
        except AttributeError:
            # chain up
            return super().pyre_identify(authority=authority, **kwds)
        # otherwise, invoke the handler
        return handler(location=self, **kwds)

    def pyre_clone(self, at: typing.Optional[pyre.primitives.pathlike] = None, **kwds):
        """
        Make as faithful a clone of mine as possible
        """
        # if the user didn't choose a {location}
        if at is None:
            # use mine
            at = self.pyre_location
        # invoke my constructor
        return super().pyre_clone(at=at, **kwds)


# end of file
