# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# map of channel names to the their inventory
class Index(dict):
    """
    A map from the names of channels to their shared inventory
    """


    # interface
    def lookup(self, name):
        """
        Look up the given channel {name} and return the associated inventory
        """
        # if the {name} is already know
        if name in self:
            # retrieve the associated inventory and return it
            return self[name]

        # otherwise, instantiate one
        inventory = self.inventoryType()

        # cascade: use '.' as the separator
        separator = '.'
        # take the name apart
        fragments = name.split(separator)
        # while there are still part to process
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
    def __init__(self, inventoryType):
        # chain up
        super().__init__()
        #  save the inventory type
        self.inventoryType = inventoryType
        # all done
        return


# end of file
