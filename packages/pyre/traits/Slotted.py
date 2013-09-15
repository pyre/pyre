# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# superclass
from .Trait import Trait


# declaration
class Slotted(Trait):
    """
    Intermediate class that knows that trait values are held by framework slots
    """


    # framework data
    isConfigurable = True # slotted traits have configurable values
    classSlot = None # the factory for class slots
    instanceSlot = None # the factory of instance slots


    # meta-methods
    def __get__(self, instance, cls):
        """
        Retrieve the value of this trait
        """
        # find out whose inventory we are supposed to access
        configurable = instance or cls
        # get the slot from the client's inventory
        slot = configurable.pyre_inventory[self]
        # compute and return its value
        return slot.value


    # implementation details
    class factory:
        """
        A factory of slots of a given trait
        """

        # meta-methods
        def __init__(self, trait, processor, **kwds):
            # chain up
            super().__init__(**kwds)
            # save my parts
            self.trait = trait
            self.processor = processor
            # all done
            return

        def __call__(self, **kwds):
            """
            Make a slot for my client trait
            """
            # build a slot and return it
            return self.trait.macro(postprocessor=self.processor, **kwds)


# end of file 
