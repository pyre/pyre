# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import collections  # access to defaultdict and OrderedDict
from .AbstractMetaclass import AbstractMetaclass


class AttributeClassifier(AbstractMetaclass):
    """
    A base metaclass that enables attribute classificiation by category. The category value to
    be used for the classification is assumed to be metadata attached to the attributes
    themselves, stored in a variable called pyre_category. Further, the declaration order of
    the attributes is retained.

    For a non-trivial example see pyre.components.Requirement and its descendants, which detect
    traits and public interface declarations, or pyre.xml.DTD, which scans Document class
    records for element declarations.

    implementation details:
      __prepare__: creates and returns a special dictionary that remembers the declaration
      order and performs the categorization on the fly, as attributes are encountered in the
      class record.

      __new__: gets the name of the class being built, its list of bases and an instance of the
      special attribute dictionary. It is responsible for building the class record.
    """


    # meta methods
    @classmethod
    def __prepare__(cls, name, bases, *, classifier, **kwds):
        """
        Build a special attribute table that classifies attributes based on their category. 

        parameters:
          {cls}: the metaclass invoked; guaranteed to be an AttributeClassifier descendant
          {name}: the name of the class being built
          {bases}: the tuple of base class records
          {classifier}: the name of the variable that holds the attribute category
        """

        # if __debug__:
            # use journal to generate debugging output
            # import journal
            # debug = journal.debug("pyre.patterns.attribute-classifier")
            # debug.line("{0.__name__}.__prepare__: name={1!r}".format(cls, name))
            # debug.line("    bases:", bases)
            # debug.log("    classifier:", classifier)

        # access through cls in case descendants have overriden Filter with their own
        return cls._pyre_AttributeFilter(classifier)


    def __new__(cls, name, bases, attributes, *, index=None, **kwds):
        """
        Build the class record

        parameters:
          {cls}: the metaclass invoked; guaranteed to be an AttributeClassifier descendant
          {name}: the name of the class being built
          {bases}: the tuple of base class records
          {index}: the name of the variable that will hold the category index
        """

        # if __debug__:
            # use journal to generate the output
            # import journal
            # debug = journal.debug("pyre.patterns.attribute-classifier")
            
            # debug.line("{0.__name__}.__new__: name={1!r}".format(cls, name))
            # debug.line("    bases:", bases)
            # debug.log("    attributes:", attributes)

        # let type build the class record
        # build a new dict for attributes so the Filter instance doesn't hang around
        record = super().__new__(cls, name, bases, dict(attributes))

        # if i was told where to deposit the category index
        if index is not None:
            # build it
            categoryIndex = cls._pyre_buildCategoryIndex(record, index, attributes)
            # and attach it to the record
            setattr(record, index, categoryIndex)

        return record


    @classmethod
    def _pyre_buildCategoryIndex(cls, record, index, attributes):
        """
        Attach the category index to the class record as the attribute index
        
        parameters:
          {record}: the class record being built
          {index}: the name of the attribute that will hold the category index
          {attributes}: attribute storage that holds the category index
       """
        # return the attribute categories 
        return attributes.categories


    # helper
    class _pyre_AttributeFilter(collections.OrderedDict):
        """
        A dictionary that filters and bins attributes that have a declared category
        """


        # interface
        def decorateDescriptor(self, name, descriptor, category):
            """
            Attach any further metadata to the descriptor being declared
            """
            return descriptor


        # meta methods
        def __init__(self, classifier):
            super().__init__()
            self.classifier = classifier
            self.categories = collections.defaultdict(list)
            return


        def __setitem__(self, name, descriptor):
            """
            Insert (name, descriptor) in the dictionary. Look for the classifier attribute in
            every incoming descriptor and bin accordingly if it exists.
            """

            # store the descriptor
            super().__setitem__(name, descriptor)

            # recognize its category and handle appropriately
            try:
                category = getattr(descriptor, self.classifier)
            except AttributeError:
                return

            # add the descriptor to the appropriate pile
            self.categories[category].append(descriptor)

            # allow descendants to further decorate the attribute descriptor
            self.decorateDescriptor(name, descriptor, category)

            return

    
# end of file 
