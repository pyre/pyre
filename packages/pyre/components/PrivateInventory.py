# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# externals
import itertools
from .. import tracking
# superclass
from .Inventory import Inventory


# declaration
class PrivateInventory(Inventory):
    """
    Strategy for managing the state of component classes and instances that were not given a
    publicly visible name, hence they are responsible for managing their own private state
    """

    # constants
    key = None # components with private inventories have no keys


    # slot access
    def setTrait(self, trait, factory, value, **kwds):
        """
        Set the value of the slot associated with {trait}
        """
        # grab the old slot
        old = self[trait]
        # use the factory to make a new slot
        new = factory(value=value)
        # replace references to the old slot
        new.replace(old)
        # and attach the new one
        self[trait] = new
        # all done
        return


    # support for building component classes and instances
    @classmethod
    def initializeClass(cls, component, **kwds):
        """
        Build inventory appropriate for a component class that is not registered with the
        nameserver
        """
        # register with the component registrar
        component.pyre_registrar.registerComponentClass(component=component)
        # invoke the registration hook
        component.pyre_classRegistered()

        # collect the slots
        local = cls.localSlots(component=component)
        inherited = cls.inheritedSlots(component=component)
        slots = itertools.chain(local, inherited)

        # build the inventory
        inventory = cls(slots=slots)
        # attach it
        component.pyre_inventory = inventory

        # invoke the configuration hook
        component.pyre_classConfigured()

        # return the inventory
        return inventory


    @classmethod
    def initializeInstance(cls, instance, **kwds):
        """
        Build inventory appropriate for a component instance that is not registered with the
        nameserver
        """
        # register with the component registrar
        cls.pyre_registrar.registerComponentInstance(instance=instance)
        # invoke the registration hook
        instance.pyre_registered()

        # build the inventory out of the instance slots and attach it
        instance.pyre_inventory = cls(slots=cls.instanceSlots(instance=instance))

        # invoke the configuration hook
        instance.pyre_configurationErrors += instance.pyre_configured()

        # all done
        return


    @classmethod
    def localSlots(cls, component):
        """
        Build slots for the locally declared traits of a {component} class
        """
        # go through the traits declared locally in {component}
        for trait in component.pyre_localTraits:
            # skip the non-configurable ones
            if not trait.isConfigurable: continue
            # yield a (trait, slot) pair
            yield trait, trait.classSlot(value=trait.default)
        # all done
        return


    @classmethod
    def inheritedSlots(cls, component):
        """
        Build slots for the inherited traits of a {component} class
        """
        # collect the traits I am looking for
        traits = set(trait for trait in component.pyre_inheritedTraits if trait.isConfigurable)
        # if there are no inherited traits, bail out
        if not traits: return
        # go through each of the ancestors of {component}
        for ancestor in component.pyre_pedigree[1:]:
            # and all its configurable traits
            for trait in ancestor.pyre_configurables():
                # if the trait is not in the target pile
                if trait not in traits:
                    # no worries; it must have been seen while processing a  closer ancestor
                    continue
                # otherwise, remove it from the target list
                traits.remove(trait)
                # get the associated slot
                slot = ancestor.pyre_inventory[trait]
                # build a reference to it; no need to switch postprocessor here, since the type
                # of an inherited trait is determined by the nearest ancestor that declared it
                ref = slot.ref(postprocessor=trait.classSlot.processor)
                # and yield the trait, slot pair
                yield trait, ref
            # if we have exhausted the trait pile
            if not traits:
                # skip the rest of the ancestors
                break
        # if we ran out of ancestors before we ran out of traits
        else:
            # complain
            missing = ', '.join('{!r}'.format(trait.name) for trait in traits)
            msg = "{}: could not locate slots for the following traits: {}".format(
                component, missing)
            # by accessing the journal package
            import journal
            # and raising a firewall, since this is almost certainly a bug
            raise journal.firewall("pyre.components").log(msg)

        # otherwise, we are done
        return


    @classmethod
    def instanceSlots(cls, instance):
        """
        Build slots for the initial inventory of an instance by building references to all the
        slots in the inventory of its class
        """
        # get the class record of this {instance}
        component = type(instance)
        # go through all the configurable traits in {component}
        for trait in component.pyre_configurables():
            # ask the class inventory for the slot that corresponds to this trait
            slot = component.pyre_inventory[trait]
            # build a reference to the class slot
            ref = slot.ref(key=None, postprocessor=trait.instanceSlot.processor)
            # hand the trait, slot pair
            yield trait, ref
        # all done
        return


    def __str__(self):
        return "public inventory at {:#x}".format(id(self))


# end of file
