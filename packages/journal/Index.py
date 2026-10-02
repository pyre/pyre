# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# the shared state of the channels
from .Inventory import Inventory


# map of channel names to their inventory
class Index(dict):
    """
    A map from the names of channels to their shared inventory, along with the severity wide
    defaults
    """

    # interface
    def lookup(self, name):
        """
        Look up the given channel {name} and return the associated inventory
        """
        # if the {name} is already known
        if name in self:
            # retrieve the associated inventory and return it
            return self[name]

        # otherwise, make one in the severity wide default state
        inventory = Inventory(active=self.active, fatal=self.fatal)

        # cascade: use '.' as the separator
        separator = "."
        # take the name apart
        fragments = name.split(separator)
        # while there are still parts to process
        while fragments:
            # pop the last portion
            fragments.pop()
            # form the new name
            candidate = separator.join(fragments)
            # if i know the {candidate}
            if candidate in self:
                # make my new {inventory} a copy of this ancestor
                inventory.copy(source=self[candidate])
                # and bail
                break

        # add it to the pile
        self[name] = inventory

        # all done
        return inventory

    # metamethods
    def __init__(self, active, fatal, device=None, **kwds):
        # chain up; {kwds} stays out of the map, since its content would become channel names
        super().__init__()
        # the default activation state of the channels of this severity
        self.active = active
        # whether they are fatal by default
        self.fatal = fatal
        # and the severity wide device; {None} defers to the chronicler
        self.device = device
        # all done
        return


# end of file
