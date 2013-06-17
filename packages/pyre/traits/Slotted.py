# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
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


    # meta-methods
    def __init__(self, classSlot=None, instanceSlot=None, **kwds):
        # chain up
        super().__init__(**kwds)
        # save my parts
        self.classSlot = classSlot or self.factory(trait=self, processor=self.coerce)
        self.instanceSlot = instanceSlot or self.factory(trait=self, processor=self.coerce)
        # all done
        return


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
            self.macro = trait.macro
            self.processor = processor
            # all done
            return

        def __call__(self, postprocessor=None, **kwds):
            """
            Make a slot for my client trait
            """
            # figure out which postprocessor I am supposed to use
            processor = postprocessor or self.processor
            # build a slot and return it
            return self.macro(postprocessor=processor, **kwds)


# end of file 
