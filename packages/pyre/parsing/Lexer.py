# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


import re
import collections
from .Token import Token
from .TokenDescriptor import TokenDescriptor


class Lexer(type):
    """
    Metaclass that looks through a Scanner class record to convert TokenDescriptors into Token
    classes and build the Scanner's regular expression engine
    """


    # constants
    pyre_TOKEN_INDEX = "pyre_tokens"


    # meta methods
    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        """
        Build an attribute table that maintains a category index for attribute descriptors
        """
        return collections.OrderedDict()


    def __new__(cls, name, bases, attributes, **kwds):
        """
        Build the document class record
        """
        # initialize the list of descriptors
        harvest = []
        # loop over the attributes
        for attrname, attribute in attributes.items():
            # for attributes that are descriptors
            if isinstance(attribute, TokenDescriptor) or (
                isinstance(attribute, type) and issubclass(attribute, Token)):
                # set their name
                attribute.name = attrname
                # add them to the pile
                harvest.append(attribute)
        # save the descriptor tuple as a class attribute
        attributes[cls.pyre_TOKEN_INDEX] = tuple(harvest)
        # let type build the class record
        record = super().__new__(cls, name, bases, attributes, **kwds)
        # initialize the list of tokens
        tokens = []
        # initialize the list of recognizers harvested from the token declarations
        recognizers = []
        # visit each one of them
        for descriptor in harvest:
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
        setattr(record, cls.pyre_TOKEN_INDEX, tokens)
        # assemble and attach the regular expression
        setattr(record, "recognizer", re.compile("|".join(recognizers)))
        # return the new class record
        return record


# end of file 
