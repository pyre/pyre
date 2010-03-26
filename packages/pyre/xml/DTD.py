# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..patterns.AttributeClassifier import AttributeClassifier


class DTD(AttributeClassifier):
    """
    Metaclass that scans the class record of a Document descendant for element descriptors and
    builds the necessary machinery for parsing the XML document
    """


    # contants
    _pyre_DTD = "dtd" # the name of the attribute that holds the attribute index
    _pyre_CLASSIFIER_NAME = "_pyre_category" # the location of index key


    # meta methods
    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        """
        Create and return a container for the attributes in the class record
        """
        return super().__prepare__(name, bases, classifier=cls._pyre_CLASSIFIER_NAME, **kwds)


    def __new__(cls, name, bases, attributes, **kwds):
        """
        Build the document class record
        """
        return super().__new__(cls, name, bases, attributes, index=cls._pyre_DTD, **kwds)


    @classmethod
    def _pyre_buildCategoryIndex(cls, record, index, attributes):
        """
        Attach the category index to the class record as the attribute index

        parameters:
            {record}: the class record being decorated
            {index}: the name of the attribute that will hold the category index
            {attributes}: storage for the category index
        """
        # extract the element descriptors from the attribute categories
        descriptors = tuple(attributes.categories["elements"])
        # build a (tag -> handler) map
        index = { descriptor.name: descriptor for descriptor in descriptors }
        # now, build the dtd for each handler
        for element in descriptors:
            element.handler._nodeIndex = {
                tag: index[tag].handler for tag in element.handler.elements }
        # and the one for the actual document class
        record._nodeIndex = { tag: index[tag].handler for tag in record.elements }
        # return it so it can be bound to whatever name _pyre_DTD specifies
        return descriptors


# end of file 
