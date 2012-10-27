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
    from .PublicInventory import PublicInventory
    from .PrivateInventory import PrivateInventory
    from ..constraints.exceptions import ConstraintViolationError


    # framework data
    pyre_inventory = None # my inventory management strategy
    pyre_implements = None # the lists of protocols i implement


    # introspection
    @property
    def pyre_name(self):
        """
        Look up my name
        """
        # ask my inventory
        return self.pyre_inventory.name()


    @classmethod
    def pyre_family(cls):
        """
        Deduce my family name
        """
        # get my inventory to answer this
        return cls.pyre_inventory.name()


    @classmethod
    def pyre_package(cls):
        """
        Deduce my package name
        """
        # get my inventory to answer this
        return cls.pyre_inventory.package()


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
        return cls.pyre_registrar.components[cls]


    def pyre_slot(self, attribute):
        """
        Return the slot associated with {attribute}
        the locator of the component
        """
        # find the trait
        trait = self.pyre_trait(alias=attribute)
        # look up the slot associated with this trait and return it
        return self.pyre_inventory.getSlot(configurable=self)


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


    # meta methods
    def __new__(cls, name, key, locator, **kwds):
        # build the instance; in order to accommodate components with non-trivial constructors,
        # we have to swallow any extra arguments passed to {__new__}; unfortunately, this
        # places some restrictions on how components participate in class hierarchies: no
        # ancestor of a user component can implement a {__new__} with non-trivial signature,
        # since it will never get its arguments. Sorry...
        instance = super().__new__(cls)

        # record the locator
        instance.pyre_locator = locator

        # deduce the visibility of this instance
        visibility = cls.PrivateInventory if key is None and name is None else cls.PublicInventory
        # invoke it
        visibility.initializeInstance(instance=instance, key=key, name=name)

        # and return the new instance
        return instance


    def __init__(self, name, key, locator, **kwds):
        # only needed to swallow the extra arguments
        super().__init__(**kwds)
        # all done
        return

                                    
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
        # attempt to
        try:
            # normalize the name
            name = self.pyre_namemap[name]
        # if it's not one of my traits
        except KeyError:
            # complain
            raise AttributeError("{} has no attribute {!r}".format(self, name))
            
        # if we got this far, restart the attribute lookup using the canonical name
        # don't be smart here; let getattr do its job, which involves invoking the trait
        # descriptors if necessary
        return getattr(self, name)


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

        # find the trait
        trait = self.pyre_traitmap[canonical]
        # record the location of the caller
        locator = tracking.here(level=1)
        # set the priority
        priority = self.pyre_executive.priority.explicit()
        # set the value
        self.pyre_inventory.setTrait(
            trait=trait, strategy=trait.instanceSlot, 
            value=value, priority=priority, locator=locator)

        # all done
        return


# end of file 
