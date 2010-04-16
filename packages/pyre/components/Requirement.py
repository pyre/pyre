# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import collections
from ..patterns.AttributeClassifier import AttributeClassifier


class Requirement(AttributeClassifier):
    """
    Metaclass that enables the harvesting of trait and interface declarations
    """


    # constants
    _pyre_CLASSIFIER_NAME = "_pyre_category"
    _pyre_INVENTORY_CLASS_NAME = "_pyre_Inventory"


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
        consist of creating a nested class to hold the inevntory items, and recording the tuple
        of ancestors of {cls} that are themselves requirements.

        parameters:
            {cls}: the metaclass invoked; guaranteed to be a Requirement descendant
            {name}: the name of the class being built
            {bases}: a tuple of the base classes from which {cls} derives
            {attributes}: a _pyre_AttributeFilter instance with the {cls} attributes
        """
        # build the class record
        record = super().__new__(cls, name, bases, attributes, **kwds)
        # construct and attach the Inventory class
        cls._pyre_buildInventoryClass(record, attributes)
        # compute the ancestors that are Requirement instances
        record._pyre_ancestors = tuple(record.pyre_ancestors())
        # and return the class record
        return record


    def __init__(self, name, bases, attributes, family=None, **kwds):
        """
        Initialize the class record

        parameters:
            {self}: an instance of the metaclass invoked; guaranteed to be a Requirement descendant
            {name}: the name of the class being built
            {bases}: a tuple of the base classes from which {cls} derives
            {attributes}: a _pyre_AttributeFilter instance with the {cls} attributes
            {family}: the public name of this class
        """
        # initialize the record
        super().__init__(name, bases, attributes, **kwds)
        # record the family name
        self._pyre_family = family
        # NYI:
        #     what does family mean for components and interfaces?
        #     what to do when family names are not unique?

        #     what to do when a component derives from another, adds new traits and doesn't
        #     reset the family name? this is a problem because the extra traits are meaningless
        #     for the ancestor class, and so configuration files that provide values for them
        #     only work for the decendant class

        # so for now: leave family blank if it were not specified (rather than inheriting a
        # value from the closest ancestor); this signals the ComponentRegistrar to not build
        # configuration nodes for this class
        return


    # implementation details
    @classmethod
    def _pyre_buildInventoryClass(cls, record, attributes):
        """
        Attach the category index to the class record

        parameters:
            {cls}: the metaclass invoked; guaranteed to be a Requirement descendant
            {record}: the class being built
            {record}: the class being built
            {attributes}: attribute storage with the category index
        """
        # initialize the name of the embedded inventory class
        name = cls._pyre_INVENTORY_CLASS_NAME
        # find all direct bases that have a _pyre_Inventory attribute 
        # this must be done every time we encounter a new record because multiple inheritance
        # changes the mro, so we can't rely on the information we recorded on any of the
        # ancestors
        bases = tuple(getattr(base, name) for base in record.__bases__ if hasattr(base, name))
        # now that we have a proper list of bases, build a class that derives from all of them
        # this class gets used to build the per-instance storage for trait values
        inventory = type(name, bases, dict())
        # attach it
        setattr(record, name, inventory)
        # initialize the name map
        inventory._pyre_namemap = dict()
        # build the category index for the inventory class record
        inventory._pyre_categories = categories = collections.defaultdict(tuple)
        # transfer the trait information from the categorized attributes
        for category, traits in attributes.categories.items():
            # attach the tuple of traits of each category to the category map
            categories[category] = tuple(traits)
            # and notify all trait descriptors that they have been atatched to a configurable
            for trait in traits:
                trait.pyre_attach(configurable=record)
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
