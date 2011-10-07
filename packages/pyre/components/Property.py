# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import collections
import pyre.tracking
from .Trait import Trait


class Property(Trait):
    """
    The base class for attribute descriptors that describe a component's external state
    """


    # import the packages exposed by properties for convenince
    from .. import schema, constraints


    # public data; name, aliases and tip are inherited from Trait
    # additional state
    type = schema.object # my type; most likely one of the pyre.schema type declarators
    default = None # my default value
    optional = False # am i allowed to be uninitialized?
    converters = () # the chain of functions that are required to produce my native type
    normalizers = () # the chain of functions that convert my values to canonical form
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
                self.validators = tuple(self.validators)
            # otherwise
            else:
                # make a tuple out of the lone validator
                self.validators = (self.validators, )
        # repeat for the converters
        if self.converters is not tuple():
            # if the user placed them in a container
            if isinstance(self.converters, collections.Iterable):
                # convert it into a tuple
                self.converters = tuple(self.converters)
            # otherwise
            else:
                # make a tuple out of the lone converter
                self.converters = (self.converters, )
        # and the normalizers
        if self.normalizers is not tuple():
            # if the user placed them in a container
            if isinstance(self.normalizers, collections.Iterable):
                # convert it into a tuple
                self.normalizers = tuple(self.normalizers)
            # otherwise
            else:
                # make a tuple out of the lone normalizer
                self.normalizers = (self.normalizers, )
        # and return
        return self


    def pyre_embedLocalTrait(self, component):
        """
        Initialize the inventory of {component}
        """
        # who else?
        super().pyre_embedLocalTrait(component=component)
        # initialize the inventory of {component} with my default value
        return self.pyre_embedTrait(component=component, value=self.default)


    def pyre_embedInheritedTrait(self, component):
        """
        Initialize the {component} inventory by establishing a reference to the nearest
        ancestor that has slot for me
        """
        # who else?
        super().pyre_embedInheritedTrait(component=component)
        # loop over my pedigree looking for an ancestor that has a slot for me
        for base in component.pyre_pedigree:
            # if it's here, get the slot and bail out
            try:
                slot = base.pyre_inventory[self]
                break
            # if not, get the next
            except KeyError:
                continue
        # impossible: couldn't find the slot; what went wrong?
        else:
            import journal
            firewall = journal.firewall("pyre.components")
            raise firewall.log("UNREACHABLE")
            
        # build a reference to the ancestral slot
        reference = slot.ref()
        # and embed it
        return self.pyre_embedTrait(component=component, value=reference)


    def pyre_embedTrait(self, component, value):
        """
        Place value in the inventory of {component}
        """
        # get the configurator
        configurator = component.pyre_executive.configurator
        # and the family of the component
        family = component.pyre_family

        # build the key
        key = family + [self.name] if family else tuple()
        # transfer the default value to the configuration store
        slot = configurator.default(key=key, value=value)
        # add the component as an observer
        slot.addObserver(component)
        # attach the slot to the component inventory
        component.pyre_inventory[self] = slot

        # and return
        return self



    def pyre_bindClass(self, configurable):
        """
        Bind this trait to the {configurable} class record
        """
        # get my slot from the {configurable}
        slot = configurable.pyre_inventory[self]
        # attach my value processor
        slot.processor = self.pyre_cast
        # mark the slot as dirty
        slot.dirty = True
        # to force it to recompute its value
        return slot.getValue()

        
    def pyre_bindInstance(self, configurable):
        """
        Bind this trait to the {configurable} instance
        """
        raise NotImplementedError("NYI!")
        # get my slot from the {configurable}
        slot = configurable.pyre_inventory[self]
        # get it to compute its value
        return slot.getValue()


    # slot value access
    def pyre_setClassTrait(self, configurable, value, locator):
        """
        Set this trait of the class record {configurable} to value
        """
        raise NotImplementedError("NYI!")
        # grab the slot from the client's inventory
        slot = configurable.pyre_inventory[self]
        # let the configurator build an evaluator for {value}
        evaluator = configurable.pyre_executive.configurator.recognize(value)
        # set the value of the slot
        slot.setValue(value=evaluator, locator=locator)
        # and return
        return


    def pyre_setInstanceTrait(self, instance, value, locator):
        """
        Set this trait of {instance} to value
        """
        raise NotImplementedError("NYI!")
        # grab the slot from the client's inventory
        slot = instance.pyre_inventory[self]
        # let the configurator build an evaluator for {value}
        evaluator = instance.pyre_executive.configurator.recognize(value)
        # set the value of the slot and return it
        return slot.setValue(value=evaluator, locator=locator)


    # value transformations
    def pyre_cast(self, node, value):
        """
        Walk {value} through the casting procedure
        """
        # {None} is special; leave it alone
        if value is None: return None
        # otherwise, convert
        for converter in self.converters: value = converter(value)
        # cast
        value = self.type.pyre_cast(value)
        # normalize
        for normalizer in self.normalizers: value = normalizer(value)
        # and return the new value
        return value


    # the descriptor interface
    def __get__(self, instance, cls):
        """
        Retrieve the value of this trait
        """
        raise NotImplementedError("NYI!")
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
        raise NotImplementedError("NYI!")
        # build an appropriate locator
        locator = pyre.tracking.here(level=1)
        # call the instance value setter
        return self.pyre_setInstanceTrait(instance=instance, value=value, locator=locator)


# end of file 
