#-*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


# superclass
from .Identifier import Identifier
# metaclass
from .Schema import Schema


# base class of all h5 objects that have an address
class Location(Identifier, metaclass=Schema):
    """
    The base class for all h5 objects that have an address
    """


    # interface
    def pyre_datasets(self):
        """
        Generate a sequence of my datasets
        """
        # i don't have any
        return []


    def pyre_groups(self):
        """
        Generate a sequence of my subgroups
        """
        # i don't have any
        return []


    def pyre_locations(self):
        """
        Generate a sequence of locations among my contents
        """
        # i don't have any
        return []


    # metamethods
    def __init__(self, name=None, at=None, **kwds):
        # chain up
        super().__init__(name=name, **kwds)
        # record the location
        self.pyre_location = at if at is not None else name
        # all done
        return


    # framework hooks
    def pyre_bind(self, name):
        """
        Attach my name
        """
        # chain up
        super().pyre_bind(name=name)
        # if i don't have a location
        if self.pyre_location is None:
            # use my name as my location
            self.pyre_location = name
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


    def pyre_clone(self, at=None, **kwds):
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
