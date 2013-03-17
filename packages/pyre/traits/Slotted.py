# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
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


    # framework data
    isConfigurable = True # slotted traits are configurable


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
        configurable = instance if instance else cls
        # grab the slot from the client's inventory
        slot = configurable.pyre_inventory.getSlot(trait=self)
        # compute and return its value
        return slot.value


# end of file 
