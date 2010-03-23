# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


import re
from .Token import Token
from .TokenDescriptor import TokenDescriptor
from ..patterns.AttributeClassifier import AttributeClassifier


class Lexer(AttributeClassifier):
    """
    Metaclass that looks through a Scanner class record to convert TokenDescriptors into Token
    classes and build the Scanner's regular expression engine
    """


    # constants
    _pyre_INDEX = "_pyre_Tokens"
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
        # let type build the class record
        record = super().__new__(cls, name, bases, attributes, index=cls._pyre_INDEX, **kwds)
        # initialize the list of tokens
        tokens = []
        # initialize the list of recognizers harvested from the token declarations
        recognizers = []
        # get the token index
        tokenDescriptors = getattr(record, cls._pyre_INDEX)
        # visit each one of them
        for descriptor in tokenDescriptors:
            # extract descriptor info: the name of the class and the pattern
            tag = descriptor.name
            pattern = descriptor.pattern
            # build the recognizer
            recognizer = re.compile(pattern) if pattern else None
            # handle TokenDescriptor instances
            if isinstance(descriptor, TokenDescriptor):
                # build the default attribute list
                fields = {
                    "pattern": pattern,
                    "recognizer": recognizer,
                    "__slots__": (),
                    }
                # build a class that derives from Token out of the information in the
                # TokenDescriptor
                tokenClass = type(tag, (Token,), fields)
                # attach it to the scanner
                setattr(record, tag, tokenClass)
            # handle Token descendants
            elif issubclass(descriptor, Token):
                tokenClass = descriptor
                tokenClass.recognizer = recognizer
            # otherwise, a hit a firewall
            else:
                import journal
                journal.firewall("pyre.parsing").log("unknown token descriptor type")

            # save the token class record in the list of tokens
            tokens.append(tokenClass)
            # if this token has a recognizer
            if descriptor.pattern:
                # add it to the pile
                recognizers.append(r"(?P<{0}>{1})".format(tag, pattern))

        # replace the token index
        setattr(record, cls._pyre_INDEX, tokens)
        # assemble and attach the regular expression
        setattr(record, "recognizer", re.compile("|".join(recognizers)))
        # return the new class record
        return record


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
        # return them so it can be bound to whatever name _pyre_INDEX specifies
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
