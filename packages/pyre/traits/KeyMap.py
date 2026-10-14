# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# superclass
from .Map import Map


# declaration
class KeyMap(Map):
    """
    A map whose entries live in the configuration store, under the name of its slot
    """

    # meta-methods
    def __init__(self, key, **kwds):
        # chain up
        super().__init__(**kwds)
        # save the name of my slot
        self.name = self.trait.pyre_nameserver.getName(key)
        # all done
        return

    def __getitem__(self, name):
        """
        Retrieve the value of the entry {name}
        """
        # get the key of the entry
        key = self.map[name]
        # and ask the store for its value
        return self.trait.pyre_nameserver[key]

    # implementation details
    def insert(self, name, value, priority, locator):
        """
        Store {value} in the map under {name}
        """
        # get the store
        nameserver = self.trait.pyre_nameserver
        # build the full name of the map entry
        fullname = nameserver.join(self.name, name)
        # insert into the model
        key, _, _ = nameserver.insert(
            name=fullname, value=value, factory=self.factory, locator=locator, priority=priority
        )
        # adjust my map
        self.map[name] = key
        # all done
        return


# end of file
