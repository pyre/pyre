# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Actor import Actor
from .Configurable import Configurable


class Component(Configurable, metaclass=Actor, hidden=True):
    """
    The base class for all components
    """


    # framework data; inherited from Configurable and repeated here for clarity
    pyre_name = None # the public id of my instances
    pyre_state = None # track progress through the bootsrapping process
    pyre_namemap = None # a map of descriptor aliases to their canonical names
    pyre_localTraits = None # a tuple of all the traits in my declaration
    pyre_inheritedTraits = None # a tuple of all the traits inherited from my superclasses
    pyre_pedigree = None # a tuple of ancestors that are themselves configurables
    # component specific attributes
    pyre_inventory = None # storage for my configurable state
    pyre_family = () # my spot in the package hierarchy
    pyre_implements = None # the interface specification built at compile time by the metaclass


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
        Hook that gets invoked by the framework right before the component is decomissioned.
        The instance should release all acquired resources.
        """
        return self


    # class interface
    @classmethod
    def pyre_getPackageName(cls):
        """
        Extract the name of the package to which this component belongs

        The current implementation returns the first fragment of the component's {pyre_family}
        """
        # attempt to extract and return the leading fragment of my {pyre_family}
        try:
            return cls.pyre_family[0]
        except IndexError:
            # otherwise
            return None


    @classmethod
    def pyre_getExtent(cls):
        """
        Return the extent of this component class, i.e. the set of its instances
        """
        return cls.pyre_executive.registrar.components[cls]


    # meta methods
    def __init__(self, name, **kwds):
        # component instance registration is done by Actor.__call__,
        # the metaclass method that # invokes this constructor
        super().__init__(**kwds)
        # store my name
        self.pyre_name = name
        # access the inventory that belongs to my class record
        classInventory = type(self).pyre_inventory

        # create my inventory
        sep = self.pyre_SEPARATOR
        inventory = {}

        for trait, slot in classInventory.items():
            # build the name of the trait
            tag = sep.join([name, trait.name])
            # make a slot
            slot = trait.pyre_instanceSlot(name=tag, evaluator=slot.newReference())
            # add it to my inventory
            inventory[trait] = slot
        # and attach it
        self.pyre_inventory = inventory

        # all done for now
        return


    def __getattr__(self, name):
        """
        Trap attribute lookup errors and attempt to resolve the name in my inventory's namemap

        This makes it possible to get the value of a trait by using any of its aliases.
        """
        # attempt to resolve the attribute name by normalizing it
        try:
            canonical = self.pyre_getTraitDescriptor(alias=name).name
        except self.TraitNotFoundError as error:
            missing = AttributeError(
                "{0.__class__.__name__!r} has no attribute {1!r}".format(self, name))
            raise missing from error
        # if we got this far, restart the attribute lookup using the canonical name
        # don't be smart here; let getattr do its job, which involves invoking the trait
        # descriptors if necessary
        return getattr(self, canonical)


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


# end of file 
