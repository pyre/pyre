# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
from .. import tracking
# superclass
from .Trait import Trait


# declaration
class Slotted(Trait):
    """
    Intermediate class that knows that trait values are held by framework slots
    """


    # framework support
    def getSlot(self, configurable):
        """
        Locate the slot held by {configurable} on my behalf
        """
        # easy enough
        return configurable.pyre_inventory.getSlot(trait=self)


    def classSlot(self, model):
        """
        Hook registered with the nameserver that informs it of my macro preference and the
        correct converter to attach to new slots for component classes
        """
        # by default, build expressions and use my schema
        return (self.macro(model=model), self.coerce)
        

    def instanceSlot(self, model):
        """
        Hook registered with the nameserver that informs it of my macro preference and the
        correct converter to attach to new slots for component classes
        """
        # by default, build expressions and use my schema
        return (self.macro(model=model), self.coerce)
        

    def macro(self, model):
        """
        Return my choice of macro evaluator so the caller can build appropriate slots
        """
        # build expressions
        return model.expression


    # meta methods
    def __get__(self, instance, cls):
        """
        Retrieve the value of this trait
        """
        # find out whose inventory we are supposed to access
        client = instance if instance else cls
        # grab the slot from the client's inventory
        slot = client.pyre_inventory.getSlot(trait=self)
        # compute and return its value
        return slot.getValue(configurable=client)


    def __set__(self, instance, value):
        """
        Set the trait of {instance} to {value}
        """
        # record the location of the caller
        locator = tracking.here(level=1)
        # set the priority
        priority = instance.pyre_executive.priority.explicit()
        # set the value
        instance.pyre_inventory.setTrait(
            trait=self, strategy=self.instanceSlot,
            value=value, priority=priority, locator=locator)
        # and return
        return


# end of file 
