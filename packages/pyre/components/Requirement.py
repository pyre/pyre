# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import pyre
import collections
from ..patterns.AttributeClassifier import AttributeClassifier


class Requirement(AttributeClassifier):
    """
    Metaclass that enables the harvesting of trait and interface declarations
    """


    # constants
    _pyre_CLASSIFIER_NAME = "_pyre_category"

    # framework data
    # the component registrar; shared by  all Component and Interface subclasses
    _pyre_registrar = pyre.executive()

    # access to the base Inventory class
    # embryonic case for an invariant to simplify the metaclass implementations: all classes in
    # the mro of components and interfaces define a _pyre_Inventory so it is safe to derive one
    # for the current class from the ones in its immediate ancestors
    from .Inventory import Inventory as _pyre_Inventory


    # meta methods
    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        """
        Build the container that will hold the trait categorizations

        parameters:
            {cls}: the metaclass invoked; guaranteed to be a Requirement descendant
            {name}: the name of the class being built
            {bases}: a tuple of the base classes from which {cls} derives
        """
        # specify the attribute name that forms the basis for field classificiation and let the
        # ancestor do the heavy lifting. the actual attributes will be stored in a
        # _pyre_AttributeFilter instance, a suitable definition of which is provided below
        return super().__prepare__(name, bases, classifier=cls._pyre_CLASSIFIER_NAME, **kwds)


    def __new__(cls, name, bases, attributes, **kwds):
        """
        Build and decorate the class record

        The actual building of the class record is done by type; the decoration performed here
        consists of creating a nested class to hold the inventory items, and recording the
        tuple of ancestors of {cls} that are themselves instances of Requirement.

        parameters:
            {cls}: the metaclass invoked; guaranteed to be a Requirement descendant
            {name}: the name of the class being built
            {bases}: a tuple of the base classes from which {cls} derives
            {attributes}: a _pyre_AttributeFilter instance with the {cls} attributes
        """
        # build the class record
        configurable = super().__new__(cls, name, bases, attributes, **kwds)
        # record the class name so that _pyre_name always exists
        configurable._pyre_name = name
        # record the traits harvested from this declaration
        configurable._pyre_traits = attributes.descriptors
        # compute the ancestors that are Requirement instances
        configurable._pyre_configurables = cls._pyre_getRequirements(configurable)
        # construct the Inventory class
        inventory = cls._pyre_buildInventoryClass(configurable, bases)
        # attach it
        configurable._pyre_Inventory = inventory
        # and connect it with its traits
        cls._pyre_decorateInventoryClass(configurable, inventory, attributes)
        # all done; return the class record
        return configurable


    # implementation details
    @classmethod
    def _pyre_getRequirements(cls, configurable):
        """
        Scan the mro looking for base classes that are instances of mine
        """
        return tuple(ancestor for ancestor in configurable.__mro__ if isinstance(ancestor, cls))


    @classmethod
    def _pyre_buildInventoryClass(cls, configurable, bases):
        """
        Build the _pyre_Inventory class that is to be embedded in {configurable}

        parameters:
            {cls}: the metaclass invoked; guaranteed to be a Requirement descendant
            {configurable}: the class being built
            {bases}: the tuple of direct ancestors of {configurable}
        """
        # make a tuple of all the _pyre_Inventory classes embedded in the direct ancestors
        # this must be done every time we encounter a new record because multiple inheritance
        # changes the mro, so we can't rely on the information we have recorded previously
        inventories = tuple(base._pyre_Inventory for base in bases if isinstance(base, cls))
        # if we couldn't find any, derive from mine
        if not inventories:
            return cls._pyre_Inventory
        # now that we have a proper list of bases, build a class that derives from all of them
        # this class gets used to build the per-instance storage for trait values
        return type("_pyre_Inventory", inventories, dict())


    @classmethod
    def _pyre_decorateInventoryClass(cls, configurable, inventory, attributes):
        """
        Build the inventory namemap
        """
        # initialize the name map
        inventory._pyre_namemap = dict()
        # build the category index for the inventory class record
        inventory._pyre_categories = categories = collections.defaultdict(tuple)
        # transfer the trait information from the categorized attributes
        for category, traits in attributes.categories.items():
            # attach the tuple of traits of each category to the category map
            categories[category] = tuple(traits)
            # and notify all trait descriptors that they have been attached to a configurable
            for trait in traits:
                trait.pyre_attach(configurable)
        # all done; return the inventory class record to the caller
        return inventory


    # attribute storage; see __prepare__ above
    class _pyre_AttributeFilter(AttributeClassifier._pyre_AttributeFilter):
        """
        Storage and categorization of the declared attributes
        """

        def decorateDescriptor(self, name, descriptor, category):
            """
            Attach any further metadata to the descriptor being declared
            """
            # store the attribute name with the descriptor
            # this also decorates function declarations, but that's ok
            descriptor.name = name
            # and return it
            return descriptor
        

# end of file 
