# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2018 all rights reserved
#


# support
import pyre


# declaration
class Node(pyre.component):
    """
    Base class for entities that participate in workflows
    """


    # introspection
    def pyre_clients(self):
        """
        Print a list of the observers of each of my traits
        """
        # get my slot
        myslot = self.pyre_slot()
        # ask it to watch over all my traits
        # myslot.observe(self.pyre_inventory[trait] for trait in self.pyre_configurables())

        # show me
        observers = tuple(myslot.observers)
        # show me
        print(f"{self.pyre_spec}:")
        print(f"    observers = {observers}")
        # go through my traits
        for trait in self.pyre_configurables():
            # show me
            print(f"    trait: {trait.name}")
            # get its slot
            slot = self.pyre_inventory[trait]
            # see who's watching it
            observers = tuple(slot.observers)
            # show me
            print(f"        observers = {observers}")

        # all done
        return


# end of file
