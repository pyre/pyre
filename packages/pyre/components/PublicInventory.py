# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
import operator
import itertools
from .. import tracking
# superclass
from .Inventory import Inventory


# declaration
class PublicInventory(Inventory):
    """
    Strategy for providing access to the state of component classes and instances that were
    given a publicly visible name and use slots managed the pyre nameserver for storage.
    """


    # interface
    def name(self):
        """
        Look up the family name of my client
        """
        # get the nameserver
        nameserver = self.pyre_nameserver
        # ask it for my full name
        _, name = nameserver.lookup(key=self.key)
        # and return it
        return name


    def package(self):
        """
        Return the package associated with this client
        """
        # get the nameserver
        nameserver = self.pyre_nameserver
        # ask it for my full name
        _, name = nameserver.lookup(key=self.key)
        # split it apart; the package name is the zeroth entry
        packageName = nameserver.split(name)[0]
        # use the name to look up the package
        return nameserver[packageName]


    # slot access
    def getSlot(self, trait):
        """
        Retrieve the slot associated with {trait}
        """
        # get the key
        key = self[trait]
        # ask the nameserver
        slot, _ = self.pyre_nameserver.lookup(key)
        # and return the slot
        return slot


    def setTrait(self, trait, strategy, value, priority, locator):
        """
        Set the value of the slot associated with {trait}
        """
        # get my key
        key = self.key
        # get the nameserver
        nameserver = self.pyre_nameserver
        # unpack the slot part
        macro, converter = strategy(model=nameserver)
        # hash the trait name
        traitKey = key[trait.name]
        # build a slot to hold value
        new = macro(
            key=traitKey, converter=converter,
            value=value, priority=priority, locator=locator)
        # adjust the model
        nameserver.insert(name=None, key=traitKey, node=new)
        # all done
        return


    # support for constructing component classes and instances
    @classmethod
    def initializeClass(cls, component, family, **kwds):
        """
        Build inventory appropriate for a component class that is registered with the
        nameserver
        """
        # get the locator
        locator = component.pyre_locator
                               
        # register the class with the executive
        key = component.pyre_executive.registerComponentClass(family=family, component=component)
        # register with the component registrar
        component.pyre_registrar.registerComponentClass(component=component)
        # invoke the registration hook
        component.pyre_classRegistered()

        # collect the slots
        local = cls.localSlots(key=key, component=component, locator=locator)
        inherited = cls.inheritedSlots(key=key, component=component, locator=locator)
        slots = itertools.chain(local, inherited)
        # make sure we build class slots
        strategy = operator.attrgetter('classSlot')
        # register them with the nameserver
        slots = cls.registerSlots(key=key, slots=slots, strategy=strategy)

        # build the inventory
        inventory = cls(key=key, slots=slots)
        # attach it
        component.pyre_inventory = inventory

        # configure the class
        component.pyre_configurator.configureComponentClass(component=component)
        # invoke the configuration hook
        component.pyre_classConfigured()

        # return the inventory
        return inventory


    @classmethod
    def initializeInstance(cls, instance, name):
        """
        Build inventory appropriate for a component instance that is not registered with the
        nameserver
        """
        # have the executive make a key
        key = cls.pyre_executive.registerComponentInstance(instance=instance, name=name)

        # register with the component registrar
        cls.pyre_registrar.registerComponentInstance(instance=instance)
        # invoke the registration hook
        instance.pyre_registered()

        # build the instance slots
        slots = cls.instanceSlots(key=key, instance=instance)
        # make sure we build instance slots
        strategy = operator.attrgetter('instanceSlot')
        # register them
        slots = cls.registerSlots(key=key, slots=slots, strategy=strategy)
        # build the inventory out of the instance slots and attach it
        instance.pyre_inventory = cls(key=key, slots=slots)

        # configure the instance
        cls.pyre_configurator.configureComponentInstance(instance=instance)
        # invoke the configuration hook
        instance.pyre_configured()

        # all done
        return


    @classmethod
    def localSlots(cls, key, component, locator):
        """
        Build slots for the locally declared traits of a {component} class
        """
        # get the nameserver
        nameserver = cls.pyre_nameserver
        # get the factory of priorities in the {defaults} category
        priority = nameserver.priority.defaults
        # go through the traits declared locally in {component}
        for trait in component.pyre_localTraits:
            # skip the non-configurable ones
            if not trait.isConfigurable: continue
            # ask the trait for the evaluation strategy details
            macro, converter = trait.classSlot(model=nameserver)
            # use it to build the slot
            slot = macro(
                key=key[trait.name], value=trait.default, converter=converter,
                priority=priority(), locator=locator)
            # yield the trait, slot pair
            yield trait, slot
        # all done
        return


    @classmethod
    def inheritedSlots(cls, key, component, locator):
        """
        Build slots for the inherited traits of a {component} class
        """
        # get the nameserver
        nameserver = cls.pyre_nameserver
        # get the factory of priorities in the {defaults} category
        priority = nameserver.priority.defaults
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
                slot = trait.getSlot(configurable=ancestor)
                # build a reference to it; no need to switch converters here, since the type of
                # an inherited trait is determined by the nearest ancestor that declared it
                ref = slot.ref(key=key[trait.name], locator=locator, priority=priority())
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
    def instanceSlots(cls, key, instance):
        """
        Build slots for the initial inventory of an instance by building references to all the
        slots in the inventory of its class
        """
        # get the component class of this {instance}
        component = type(instance)
        # get the nameserver
        nameserver = cls.pyre_nameserver
        # get the locator
        locator = instance.pyre_locator
        # get the factory of priorities in the {defaults} category
        priority = nameserver.priority.defaults
        # go through all the configurable traits in {component}
        for trait in component.pyre_configurables():
            # ask the class inventory for the slot that corresponds to this trait
            slot = component.pyre_inventory.getSlot(trait=trait)
            # and its slot strategy
            _, converter = trait.instanceSlot(model=nameserver)
            # build a reference to the class slot
            ref = slot.ref(
                key=key[trait.name], converter=converter, locator=locator, priority=priority())
            # hand the trait, slot pair
            yield trait, ref
        # all done
        return


    @classmethod
    def registerSlots(cls, key, slots, strategy):
        """
        Go through the (trait, slot) pairs in {slots} and register them with the nameserver
        """
        # get the nameserver
        nameserver = cls.pyre_nameserver
        # look up the basename
        _, base = nameserver.lookup(key)
        # go through the (trait, slot) pairs
        for trait, slot in slots:
            # get the name of the trait
            traitName = trait.name
            # build the trait key
            traitKey = key[traitName]
            # register this key as belonging to a trait
            nameserver.registerTrait(key=traitKey, strategy=strategy(trait))
            # build the trait fill name
            fullname = nameserver.join(base, traitName)
            # place the slot with the nameserver 
            nameserver.insert(name=fullname, key=traitKey, node=slot)
            # register the trait aliases
            for alias in trait.aliases:
                # skip the canonical name
                if alias == traitName: continue
                # notify the nameserver
                nameserver.alias(base=key, alias=alias, target=traitKey)
            # hand this (trait, key) pair to the caller
            yield trait, traitKey
        # all done
        return
            

    # meta-methods
    def __init__(self, key, **kwds):
        super().__init__(**kwds)
        self.key = key
        return


    def __str__(self):
        return "public inventory at {:#x}".format(id(self))


# end of file 
