# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import itertools
from .. import tracking
# superclass
from .Configurable import Configurable
# metaclass
from .Actor import Actor


# class declaration
class Component(Configurable, metaclass=Actor, internal=True):
    """
    The base class for all components
    """


    # types
    from ..constraints.exceptions import ConstraintViolationError


    # framework data
    pyre_implements = None # the lists of protocols i implement


    # framework notifications
    def pyre_registered(self):
        """
        Hook that gets invoked by the framework after the component instance has been
        registered but before any configuration events
        """
        return self


    def pyre_configured(self):
        """
        Hook that gets invoked by the framework after the component instance has been
        configured but before the binding of any of its traits
        """
        return self


    def pyre_bound(self):
        """
        Hook that gets invoked by the framework after all the properties of this component
        instance have been assigned their final values, but before any validation has been
        performed
        """
        return self


    def pyre_validated(self):
        """
        Hook that gets invoked by the framework after the properties of this component instance
        have been validated. It is an opportunity to perform checks that involve the values of
        more than one property at a time, and hence could not have been attached to any one
        property
        """
        return self


    def pyre_initialized(self):
        """
        Hook that gets invoked by the framework right before the component is put into
        action. The component is now in a known good state, with all configurable traits fully
        bound and validated. This is the place where the component should acquire whatever
        further resources it requires.
        """
        return self


    def pyre_finalized(self):
        """
        Hook that gets invoked by the framework right before the component is decommissioned.
        The instance should release all acquired resources.
        """
        return self


    # introspection
    @classmethod
    def pyre_getExtent(cls):
        """
        Return the extent of this class, i.e. the set of its instances
        """
        # the registrar knows
        return cls.pyre_executive.registrar.components[cls]


    def pyre_slot(self, attribute):
        """
        Return the slot associated with {attribute}
        the locator of the component
        """
        # find the trait
        trait = self.pyre_trait(alias=attribute)
        # look up the slot associated with this trait and return it
        return trait.getSlot(configurable=self)


    def pyre_where(self, attribute=None):
        """
        Return the locator associated with {attribute}; if no attribute name is given, return
        the locator of the component
        """
        # if no name is given, return my locator
        if attribute is None: return self.pyre_locator
        # otherwise, find the slot
        slot = self.pyre_slot(attribute=attribute)
        # and return its locator
        return slot.locator


    # implementation details; don't use these
    @classmethod
    def pyre_buildClassInventory(cls):
        """
        Build the component inventory, a map from trait descriptors to the configuration slots
        that hold the trait values
        """
        # get my registration key
        me = cls.pyre_key

        # make a locator
        this = tracking.simple('during the initialization of {}'.format(cls))
        locator = tracking.chain(this=this, next=cls.pyre_locator)

        # get my local slots
        localSlots = cls.pyre_buildLocalSlots(key=me, locator=locator)
        # and references to my inherited slots
        inheritedSlots = cls.pyre_buildInheritedSlots(key=me, locator=locator)

        # if i am not registered with the nameserver
        if me is None:
            # we must build local storage for the trait values
            inventory = {}
            # insert the local traits
            inventory.update(localSlots)
            # and references to ancestral slots for my inherited traits
            inventory.update(inheritedSlots)
            # all done
            return inventory

        # otherwise, get my family name
        family = cls.pyre_family()
        # get the nameserver
        ns = cls.pyre_executive.nameserver
        # go through all the slots
        for trait, slot in itertools.chain(localSlots, inheritedSlots):
            # get the name of the trait
            name = trait.name
            # build the trait key
            key = me[name]
            # register this key as belonging to a trait
            ns.registerTrait(key=key, strategy=trait.classSlot)
            # build the trait full name
            fullname = ns.join(family, name)
            # add the slot to the nameserver model
            ns.insert(name=fullname, key=key, node=slot)
            # and register my aliases
            for alias in trait.aliases:
                # skip my canonical name
                if alias == name: continue
                # make it happen
                ns.alias(base=me, alias=alias, target=key)

        # indicate that this class does not need local storage for its traits
        return None


    @classmethod
    def pyre_buildInstanceInventory(cls, instance):
        """
        Build the component inventory, a map from trait descriptors to the configuration slots
        that hold the trait values
        """
        # get my registration key
        me = instance.pyre_key

        # make a locator
        this = tracking.simple('during the instantiation of {}'.format(cls))
        locator = tracking.chain(this=this, next=cls.pyre_locator)

        # get my local slots
        slots = cls.pyre_buildReferences(key=me, locator=locator)

        # if i am not registered with the nameserver
        if me is None:
            # we must build local storage for the trait values
            inventory = {}
            # insert the local traits
            inventory.update(slots)
            # all done
            return inventory

        # get the nameserver
        ns = cls.pyre_executive.nameserver
        # go through all the slots
        for trait, slot in slots:
            # get the name of the trait
            name = trait.name
            # build the trait key
            key = me[name]
            # register this key as belonging to a trait
            ns.registerTrait(key=key, strategy=trait.instanceSlot)
            # build the trait full name
            fullname = ns.join(instance.pyre_name, name)
            # add the slot to the nameserver model
            ns.insert(name=fullname, key=key, node=slot)
            # and register my aliases
            for alias in trait.aliases:
                # skip my canonical name
                if alias == name: continue
                # make it happen
                ns.alias(base=me, alias=alias, target=key)

        # indicate that this instance does not need local storage for its traits
        return None


    @classmethod
    def pyre_buildLocalSlots(cls, key, locator):
        """
        Build slots for the local traits
        """
        # get the nameserver
        ns = cls.pyre_executive.nameserver
        # the factory of priorities in the {defaults} category
        priority = ns.priority.defaults
        # go through my locally declared traits
        for trait in cls.pyre_localTraits:
            # skip the non configurable ones, e.g. behaviors, for which we don't build slots
            if not trait.isConfigurable: continue
            # ask the trait for its evaluation strategy
            macro, converter = trait.classSlot(model=ns)
            # use to build the slot
            slot = macro(
                key=None if key is None else key[trait.name],
                value=trait.default, priority=priority(), locator=locator, converter=converter)
            # yield the pair
            yield trait, slot
        # all done
        return


    @classmethod
    def pyre_buildInheritedSlots(cls, key, locator):
        """
        Build references to ancestor slots for my inherited traits
        """
        # get the nameserver
        ns = cls.pyre_executive.nameserver
        # the factory of priorities in the {defaults} category
        priority = ns.priority.defaults
        # the traits i am looking for
        traits = set(trait for trait in cls.pyre_inheritedTraits if trait.isConfigurable)
        # go through each of my ancestors
        for ancestor in cls.pyre_pedigree[1:]:
            # and all its configurable traits
            for trait in ancestor.pyre_configurables():
                # if the trait is not in the target pile
                if trait not in traits:
                    # no worries, it must have been processed already by a closer ancestor
                    continue
                # otherwise, remove it from the target set
                traits.remove(trait)
                # get the associated slot
                slot = trait.getSlot(configurable=ancestor)
                # build a reference to it
                ref = slot.ref(
                    key=None if key is None else key[trait.name],
                    locator=locator, priority=priority())
                # and yield the pair
                yield trait, ref
            # if we have exhausted the set of traits we are looking for
            if not traits:
                # skip the rest of the ancestors
                break
        # if we ran out ancestors before we ran out of traits
        else:
            # complain
            missing = ', '.join('{!r}'.format(trait.name) for trait in traits)
            msg = "{}: could not locate slots for the following traits: {}".format(
                cls, missing)
            # by raising a firewall, since this is almost certainly a bug
            import journal
            raise journal.firewall("pyre.components").log(msg)

        # otherwise, we are done
        return


    @classmethod
    def pyre_buildReferences(cls, key, locator):
        """
        Build references to the class inventory slots
        """
        # get the nameserver
        ns = cls.pyre_executive.nameserver
        # the factory of priorities in the {defaults} category
        priority = ns.priority.defaults
        # go through all my configurable traits
        for trait in cls.pyre_configurables():
            # ask the trait for its slot
            slot = trait.getSlot(configurable=cls)
            # and its slot strategy
            _, converter = trait.instanceSlot(model=ns)
            # build a reference to it for the caller
            ref = slot.ref(
                key=None if key is None else key[trait.name],
                locator=locator, priority=priority(), converter=converter)
            # send the (trait, reference) pair to my caller
            yield trait, ref
        # all done
        return


    # meta methods
    def __new__(cls, locator, name=None, key=None, **kwds):
        # build the instance
        instance = super().__new__(cls, **kwds)

        # record the locator
        instance.pyre_locator = locator

        # get the executive
        executive = cls.pyre_executive

        # if no key was specified
        if key is None and name is not None:
            # register with the executive
            instance.pyre_key = executive.registerComponentInstance(
                component=instance, name=name, locator=locator)
        # otherwise
        else:
            # just use what i was given; this happens only when this component has been
            # instantiated implicitly as the trait of another component
            instance.pyre_key = key
        # register with the component registrar
        executive.registrar.registerComponentInstance(instance=instance)
        # invoke the registration hook
        instance.pyre_registered()

        # build the instance inventory
        instance.pyre_inventory = cls.pyre_buildInstanceInventory(instance)
        # if the instance has a registration key
        if instance.pyre_key:
            # configure it
            executive.configurator.configureComponentInstance(instance=instance)
        # invoke the registration hook
        instance.pyre_configured()

        # return the instance
        return instance


    def __str__(self):
        # accumulate the name fragments here
        fragments = []
        # get my name
        name = self.pyre_name
        # if i have one:
        if name is not None:
            # use it
            fragments.append('component {!r}'.format(self.pyre_name))
        # otherwise, get my family name
        family = self.pyre_family()
        # if i have one
        if family:
            # use it
            fragments.append('instance of {!r} at {:#x}'.format(family, id(self)))
        # otherwise
        else:
            # leave a marker
            fragments.append('instance of {!r} at {:#x}'.format(type(self).__name__, id(self)))
        # assemble
        return ', '.join(fragments)


    def __getattr__(self, name):
        """
        Trap attribute lookup errors and attempt to resolve the name in my inventory's name
        map. This makes it possible to get the value of a trait by using any of its aliases.
        """
        # attempt to resolve the attribute name by normalizing it
        try:
            trait = self.pyre_trait(alias=name)
        except self.TraitNotFoundError as error:
            # build the exception
            missing = AttributeError("{} has no attribute {!r}".format(self, name))
            # and raise it
            raise missing
        # if we got this far, restart the attribute lookup using the canonical name
        # don't be smart here; let getattr do its job, which involves invoking the trait
        # descriptors if necessary
        return getattr(self, trait.name)


    def __setattr__(self, name, value):
        """
        Trap attribute retrieval and attempt to normalize the name before making the assignment
        """
        # attempt to
        try:
            # normalize the name
            canonical = self.pyre_namemap[name]
        # if the name is not in the name map
        except KeyError:
            # this must a non-trait attribute
            return super().__setattr__(name, value)
        # try again with the normalized name
        return super().__setattr__(canonical, value)


# end of file 
