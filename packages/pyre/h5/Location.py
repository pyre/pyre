#-*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2022 all rights reserved


# superclass
from .Identifier import Identifier
# metaclass
from .Schema import Schema
# my parts
from .Inventory import Inventory


# base class of all h5 objects that have an address
class Location(Identifier, metaclass=Schema):
    """
    The base class for all h5 objects that have an address
    """


    # metamethods
    def __init__(self, name=None, at=None, **kwds):
        # chain up
        super().__init__(name=name, **kwds)
        # record the location
        self.pyre_location = at if at is not None else name
        # initialize my inventory
        self.pyre_inventory = Inventory()
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


# end of file
