# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
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


    # interface
    def name(self):
        """
        Return the name of my client
        """
        # private components have no name
        return None


    def package(self):
        """
        Return the package associated with this client
        """
        # private components have no packages
        return None


    # slot access
    def getSlot(self, trait):
        """
        Retrieve the slot associated with {trait}
        """
        # easy enough
        return self[trait]


    def setTrait(self, trait, strategy, value, priority, locator):
        """
        Set the value of the slot associated with {trait}
        """
        # get the nameserver
        ns = self.pyre_nameserver
        # unpack the slot part
        macro, converter = strategy(model=ns)
        # build the slot
        new = macro(key=None, converter=converter, value=value, locator=locator, priority=priority)
        # get the old slot 
        old = self[trait]
        # pick the winner of the two
        winner = ns.node.select(model=ns, existing=old, replacement=new)
        # if the new slot is the winner
        if new is winner:
            # update the inventory
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
        # make a locator
        locator = component.pyre_locator
                               
        # register with the component registrar
        component.pyre_registrar.registerComponentClass(component=component)
        # invoke the registration hook
        component.pyre_classRegistered()

        # collect the slots
        local = cls.localSlots(component=component, locator=locator)
        inherited = cls.inheritedSlots(component=component, locator=locator)
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
        instance.pyre_configured()

        # all done
        return


    @classmethod
    def localSlots(cls, component, locator):
        """
        Build slots for the locally declared traits of a {component} class
        """
        # get the nameserver
        ns = cls.pyre_nameserver
        # get the factory of priorities in the {defaults} category
        priority = ns.priority.defaults
        # go through the traits declared locally in {component}
        for trait in component.pyre_localTraits:
            # skip the non-configurable ones
            if not trait.isConfigurable: continue
            # ask the trait for the evaluation strategy details
            macro, converter = trait.classSlot(model=ns)
            # use it to build the slot
            slot = macro(
                key=None, value=trait.default, converter=converter,
                priority=priority(), locator=locator)
            # yield the trait, slot pair
            yield trait, slot
        # all done
        return


    @classmethod
    def inheritedSlots(cls, component, locator):
        """
        Build slots for the inherited traits of a {component} class
        """
        # get the nameserver
        ns = cls.pyre_nameserver
        # get the factory of priorities in the {defaults} category
        priority = ns.priority.defaults
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
                slot = ancestor.pyre_inventory.getSlot(trait=trait)
                # build a reference to it; no need to switch converters here, since the type of
                # an inherited trait is determined by the nearest ancestor that declared it
                ref = slot.ref(key=None, locator=locator, priority=priority())
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
            # by raising a firewall, since this is almost certainly a bug
            import journal
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
        # get the nameserver
        ns = cls.pyre_nameserver
        # get the locator
        locator = instance.pyre_locator
        # get the factory of priorities in the {defaults} category
        priority = ns.priority.defaults
        # go through all the configurable traits in {component}
        for trait in component.pyre_configurables():
            # ask the class inventory for the slot that corresponds to this trait
            slot = component.pyre_inventory.getSlot(trait=trait)
            # and its slot strategy
            _, converter = trait.instanceSlot(model=ns)
            # build a reference to the class slot
            ref = slot.ref(key=None, converter=converter, locator=locator, priority=priority())
            # hand the trait, slot pair
            yield trait, ref
        # all done
        return


    def __str__(self):
        return "public inventory at {:#x}".format(id(self))


# end of file 
