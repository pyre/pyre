# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Actor import Actor
from .Configurable import Configurable


class Component(Configurable, metaclass=Actor, hidden=True):
    """
    The base class for all components
    """


    # framework data; inherited from Configurable and repeated here for clarity
    pyre_name = None # the public id of my instances
    pyre_family = () # the user-visible name of my class
    pyre_namemap = None # a map of descriptor aliases to their canonical names
    pyre_localTraits = None # a tuple of all the traits in my declaration
    pyre_inheritedTraits = None # a tuple of all the traits inherited from my superclasses
    pyre_pedigree = None # a tuple of ancestors that are themselves configurables
    # component specific attributes
    pyre_inventory = None # storage for my configurable state
    pyre_implements = None # the interface specification built at compile time by the metaclass


    # types
    # exceptions
    from ..constraints.exceptions import ConstraintViolationError


    # framework notifications
    def pyre_register(self, executive):
        """
        Hook that gets invoked by the framework after the component instance has been
        registered but before any configuration events
        """
        return self


    def pyre_configure(self, executive):
        """
        Hook that gets invoked by the framework after the component instance has been
        configured but before the binding of any of its traits
        """
        return self


    def pyre_bind(self, executive):
        """
        Hook that gets invoked by the framework after all the properties of this component
        instance have been assigned their final values, but before any validation has been
        performed
        """
        return self


    def pyre_validate(self, executive):
        """
        Hook that gets invoked by the framework after the properties of this component instance
        have been validated. It is an opportunity to perform checks that involve the values of
        more than one property at a time, and hence could not have been attached to any one
        property
        """
        return self


    def pyre_initialize(self, executive):
        """
        Hook that gets invoked by the framework right before the component is put into
        action. The component is now in a known good state, with all configurable traits fully
        bound and validated. This is the place where the component should acquire whatever
        further resources it requires.
        """
        return self


    def pyre_finalize(self, executive):
        """
        Hook that gets invoked by the framework right before the component is decommissioned.
        The instance should release all acquired resources.
        """
        return self


    # class interface
    @classmethod
    def pyre_getExtent(cls):
        """
        Return the extent of this component class, i.e. the set of its instances
        """
        return cls.pyre_executive.registrar.components[cls]


    @classmethod
    def pyre_getTraitDefaultValue(cls, trait):
        """
        Look through my supeclasses for the current default value of {trait}
        """
        # look through my ancestry for the value node
        for record in cls.pyre_pedigree:
            try:
                slot = record.pyre_inventory[trait]
            except KeyError:
                continue
            else:
                return slot.value
        # if we got this far, we have a bug; report it
        import journal
        firewall = journal.firewall("pyre.components")
        raise firewall.log(
            "could not find trait {.name!r} in {.pyre_name!r}".format(trait, cls))


    # trait observation
    def pyre_updatedProperty(self, slot):
        """
        Handler invoked when the value of one of my traits changes
        """
        # ignore it, for now
        return


    def pyre_replaceSlot(self, current, replacement, clean=None):
        """
        Replace {current} with {replacement} in my inventory
        """
        # adjust my inventory
        self.pyre_inventory[current.trait] = replacement
        # and return
        return


    # meta methods
    def __init__(self, name=None, **kwds):
        # component instance registration is done by Actor.__call__, the metaclass method that
        # invokes this constructor
        super().__init__(**kwds)
        # store my name
        self.pyre_name = name if name is not None else "<component @ {:#x}>".format(id(self))
        # access the inventory that belongs to my class record
        classInventory = type(self).pyre_inventory
        # the executive
        executive = self.pyre_executive
        # and its configurator
        configurator = executive.configurator

        # create my inventory
        sep = self.pyre_SEPARATOR
        inventory = {}

        # build my configuration key
        key = name.split(sep) if name else ()

        # iterate over the items in my class inventory
        for trait, default in classInventory.items():
            # build the name of the trait
            traitkey = key + [trait.name] if key else tuple()
            # ask the configurator to register the default value
            slot = configurator.default(key=traitkey, value=default.ref())
            # record the trait
            slot.trait = trait
            # register me as an observer
            slot.componentInstance = self
            # and add it to my inventory
            inventory[trait] = slot
            # if i am registered with the configuration store
            if traitkey:
                # iterate over my aliases
                for alias in trait.aliases:
                    # avoid duplicate registration
                    if alias == trait.name: continue
                    # build the alias key
                    aliaskey = key + [alias]
                    # register it
                    configurator._alias(canonical=traitkey, alias=aliaskey)


        # attach my inventory
        self.pyre_inventory = inventory

        # register with the executive
        executive.registerComponentInstance(self)

        # all done for now
        return


    def __getattr__(self, name):
        """
        Trap attribute lookup errors and attempt to resolve the name in my inventory's name map

        This makes it possible to get the value of a trait by using any of its aliases.
        """
        # attempt to resolve the attribute name by normalizing it
        try:
            trait = self.pyre_getTraitDescriptor(alias=name)
        except self.TraitNotFoundError as error:
            # get the component family name
            family = self.pyre_SEPARATOR.join(self.pyre_family)
            # if this is a nameless one, just use the class name
            if not family: family = self.__class__.pyre_name
            # build the exception
            missing = AttributeError(
                "component {.pyre_name!r}, an instance of {!r},"
                " has no attribute {!r}".format(self, family, name))
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
        # normalize the name
        try:
            canonical = self.pyre_getTraitDescriptor(alias=name).name
        except self.TraitNotFoundError:
            return super().__setattr__(name, value)

        return super().__setattr__(canonical, value)


    # debugging
    def pyre_dump(self):
        """
        Dump out my configuration
        """
        # spit out my name
        print("{.pyre_name}: configuration".format(self))
        # spit out my class
        print("  instance of {0.pyre_name!r} from {0}".format(self.__class__))
        # print out my family
        print("  family: {!r}".format(self.pyre_SEPARATOR.join(self.pyre_family)))
        # print out my interfaces
        print("  implements:", self.pyre_implements)
        # configuration section
        print("  configuration:")
        # iterate over all my traits
        for trait in self.pyre_getTraitDescriptors():
            # skip non-inventory items (e.g. behaviors)
            if (trait in self.pyre_inventory):
                # print out the trait name
                print("    {}".format(self.pyre_getTraitFullName(trait.name)))
                # get the associated slot
                slot = self.pyre_inventory[trait]
                # the trait value
                print("      value: {!r}".format(slot.value))
                # what was the default value?
                print("      default: {!r}".format(self.pyre_getTraitDefaultValue(trait)))
                # aliases for this trait
                print("      aliases: {!r}".format(trait.aliases))
                # and its documentation string
                print("      purpose: {!r}".format(trait.doc))
                # where did this value come from?
                print("      from: {}".format(slot._locator))
                # slot.dump()

        # all done
        return


# end of file
