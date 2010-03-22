# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..patterns.AttributeClassifier import AttributeClassifier


class Lexer(AttributeClassifier):
    """
    Metaclass that looks through a Scanner class record to convert TokenDescriptors into Token
    classes and build the Scanner's regular expression engine
    """


    # constants
    _pyre_INDEX = "tokens"
    _pyre_CLASSIFIER_NAME = "_pyre_category"


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
        return super().__new__(cls, name, bases, attributes, index=cls._pyre_INDEX, **kwds)


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
        descriptors = attributes.categories["tokens"]
        # print them out
        for descriptor in descriptors:
            print(descriptor.name)
        
        # return it so it can be bound to whatever name _pyre_DTD specifies
        return descriptors


    # attribute storage
    class _pyre_AttributeFilter(AttributeClassifier._pyre_AttributeFilter):
        """
        Storage and categorization for the token declarations
        """


        def decorateDescriptor(self, name, descriptor, category):
            """
            Attach the name of the descriptor
            """
            # set the name
            descriptor.name = name
            # and return the descriptor
            return descriptor
            

# end of file 
