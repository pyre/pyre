# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import collections
import pyre.tracking
from .Trait import Trait


class Property(Trait):
    """
    The base class for attribute descriptors that describe a component's external state
    """


    # types
    from .Slot import Slot


    # import the packages exposed by properties for convenince
    from .. import schema, constraints


    # public data; name, aliases and tip are inherited from Trait
    # additional state
    type = schema.object # my type; most likely one of the pyre.schema type declarators
    default = None # my default value
    optional = False # am i allowed to be uninitialized?
    converters = () # the chain of functions that are required to produce my native type
    validators = () # the chain of functions that validate my values


    # interface
    def pyre_initialize(self):
        """
        Attach any metadata harvested by the requirement metaclass

        This gets called by Requirement, the metaclass of all configurables, as part of the
        process that constructs the class record. Don't expect {configurable} to be fully
        functioning at this point.
        """
        # do whatever my superclass requires
        super().pyre_initialize()
        # adjust the validators
        if self.validators is not tuple():
            # if the user placed them in a container
            if isinstance(self.validators, collections.Iterable):
                # convert it into a tuple
                self.validators = tuple(trait.validators)
            # otherwise
            else:
                # make a tuple out of the lone validator
                self.validators = (self.validators, )
        # repeat for the converters
        if self.converters is not tuple():
            # if the user placed them in a container
            if isinstance(self.converters, collections.Iterable):
                # convert it into a tuple
                self.converters = tuple(trait.converters)
            # otherwise
            else:
                # make a tuple out of the lone converter
                trait.converters = (trait.converters, )
        # and return
        return self


    def pyre_embedLocal(self, component):
        """
        Initialize the inventory of {component}
        """
        # who else?
        super().pyre_embedLocal(component=component)
        # build a literal evaluator to hold my default value
        evaluator = component.pyre_executive.configurator.recognize(value=self.default)
        # build a slot
        slot = self.pyre_classSlot(evaluator=evaluator)
        # attach the slot to the inventory
        component.pyre_inventory[self] = slot
        # and return
        return


    def pyre_embedInherited(self, component):
        """
        Initialize the {component} inventory by establishing a reference to the nearest
        ancestor that has slot for me
        """
        # who else?
        super().pyre_embedInherited(component=component)
        # loop over my pedigree looking for an ancestor that has a slot for me
        for base in component.pyre_pedigree:
            # if it's here, get the slot and bail out
            try:
                node = base.pyre_inventory[self]
                break
            # if not, get the next
            except KeyError:
                continue
        # impossible: couldn't find the slot; what went worng?
        else:
            import journal
            firewall = journal.firewall("pyre.components")
            raise firewall.log("UNREACHABLE")
            
        # build a reference to the slot
        evaluator = node.newReference()
        # make a slot  out of it
        slot = self.pyre_classSlot(evaluator=evaluator)
        # attach it to the inventory
        component.pyre_inventory[self] = slot
        # and return
        return


    def pyre_bindClass(self, configurable):
        """
        Bind this trait to the {configurable} class record
        """
        # get my slot from the {configurable}
        slot = configurable.pyre_inventory[self]
        # get it to compute its value
        return slot.getValue()

        
    def pyre_bindInstance(self, configurable):
        """
        Bind this trait to the {configurable} instance
        """
        # get my slot from the {configurable}
        slot = configurable.pyre_inventory[self]
        # get it to compute its value
        return slot.getValue()

        
    # slot building
    def pyre_classSlot(self, evaluator):
        """
        Create a new slot suitable for placing in a component class inventory
        """
        # make a slot with the given {evaluator}
        return self.Slot(processor=self, value=None, evaluator=evaluator)


    def pyre_instanceSlot(self, name, evaluator):
        """
        Create a new slot suitable for placing in a component instance inventory
        """
        # make a slot with the given {evaluator}
        return self.Slot(processor=self, value=None, evaluator=evaluator)


    # slot value access
    def pyre_setClassTrait(self, configurable, value, locator):
        """
        Set this trait of the class record {configurable} to value
        """
        # grab the slot from the client's inventory
        slot = configurable.pyre_inventory[self]
        # let the configurator build an evaluator for {value}
        evaluator = configurable.pyre_executive.configurator.recognize(value)
        # set the value of the slot
        slot.setValue(value=value, locator=locator)
        # and return
        return


    def pyre_setInstanceTrait(self, instance, value, locator):
        """
        Set this trait of {instance} to value
        """
        # grab the slot from the client's inventory
        slot = instance.pyre_inventory[self]
        # let the configurator build an evaluator for {value}
        evaluator = instance.pyre_executive.configurator.recognize(value)
        # set the value of the slot
        slot.setValue(value=value, locator=locator)
        # and return
        return


    # the descriptor interface
    def __get__(self, instance, cls):
        """
        Retrieve the value of this trait
        """
        # find out whose inventory we are supposed to access
        client = instance if instance else cls
        # grab the slot from the client's inventory
        slot = client.pyre_inventory[self]
        # compute and return its value
        return slot.getValue()


    def __set__(self, instance, value):
        """
        Set this trait of {instance} to {value}
        """
        # build an appropriate locator
        locator = pyre.tracking.here(level=1)
        # call the instance value setter
        return self.pyre_setInstanceTrait(instance=instance, value=value, locator=locator)


# end of file 
