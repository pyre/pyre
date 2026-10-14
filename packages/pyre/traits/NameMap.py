# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Map import Map


# declaration
class NameMap(Map):
    """
    A map that holds the slots of its entries itself, for the slots of anonymous components,
    which live outside the configuration store
    """

    def __getitem__(self, name):
        """
        Retrieve the value of the entry {name}
        """
        # get the slot
        node = self.map[name]
        # and return its value
        return node.value

    # implementation details
    def insert(self, name, value, **kwds):
        """
        Build a slot to hold {value} and place it in the map
        """
        # make a slot
        new = self.factory(value=value)
        # look for an existing slot under the same name
        try:
            # get it
            old = self.map[name]
        # if there wasn't one
        except KeyError:
            # no worries
            pass
        # if there was
        else:
            # replace the old with the new in the evaluation graph
            new.replace(old)
        # update the map
        self.map[name] = new
        # all done
        return


# end of file
