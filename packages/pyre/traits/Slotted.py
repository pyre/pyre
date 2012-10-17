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


    # setting values
    def setClassTrait(self, configurable, value, priority, locator):
        """
        Set the value of this trait for a configurable class
        """
        # delegate to the helper
        return self.setTrait(
            strategy=self.classSlot,
            configurable=configurable, value=value, priority=priority, locator=locator)


    def setInstanceTrait(self, configurable, value, priority, locator):
        """
        Set the value of this trait for a {configurable} instance
        """
        # delegate to the helper
        return self.setTrait(
            strategy=self.instanceSlot,
            configurable=configurable, value=value, priority=priority, locator=locator)


    def setTrait(self, strategy, configurable, value, priority, locator):
        """
        Support for {setClassTrait} and {setInstanceTrait}
        """
        # ask the {configurable} for its registration key
        key = configurable.pyre_key
        # get the nameserver
        ns = configurable.pyre_executive.nameserver
        # ask for parts for a class slot
        macro, converter = strategy(model=ns)

        # if it's not registered with the nameserver
        if not key:
            # build a slot to hold {value}
            new = macro(
                key=None,
                value=value, priority=priority, locator=locator, converter=converter)
            # the current slot is in its inventory
            old = configurable.pyre_inventory[self]
            # pick the winner of the two
            winner = ns.node.select(model=ns, existing=old, replacement=new)
            # if the new slot is the winner
            if new is winner:
                # update the inventory
                configurable.pyre_inventory[self] = new
            # all done
            return

        # otherwise, build a slot to hold {value}
        new = macro(
            key=key[self.name],
            value=value, priority=priority, locator=locator, converter=converter)
        # otherwise, build my registration key
        traitKey = key[self.name]
        # ask the nameserver to adjust the model
        ns.insert(name=None, key=traitKey, node=new)
        # and return
        return


    # framework support
    def getSlot(self, configurable):
        """
        Locate the slot held by {configurable} on my behalf
        """
        # careful not to make any assumptions about the nature of {configurable}
        # get its key
        key = configurable.pyre_key
        # if it doesn't exist
        if key is None:
            # my slot is inventory for this configurable
            return configurable.pyre_inventory[self]
        # otherwise, the slot is held by the nameserver
        ns = configurable.pyre_executive.nameserver
        # build the trait key and get the slot
        slot, _ = ns.lookup(key=key[self.name])
        # and return it
        return slot


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
        slot = self.getSlot(configurable=client)
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
        self.setInstanceTrait(
            configurable=instance, value=value, locator=locator, priority=priority)
        # and return
        return



# end of file 
