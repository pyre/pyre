# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2013 all rights reserved
#


# externals
import re
import collections
# my super class
from pyre.patterns.AttributeClassifier import AttributeClassifier


class Lexer(AttributeClassifier):
    """
    Metaclass that enables its instances to convert input sources into token streams
    """


    # types
    from .Token import Token as token
    from .Descriptor import Descriptor as descriptor


    # meta methods
    def __new__(cls, name, bases, attributes, **kwds):
        """
        Build the scanner class record
        """
        # print('Lexer.__new__: processing {!r}'.format(name))
        # initialize the token class list
        tokens = []
        patterns = []
        # harvest the token descriptors
        for name, descriptor in cls.pyre_harvest(attributes, cls.descriptor):
            # print('    {}: "{}"'.format(name, descriptor.pattern))
            # initialize the attributes of the token class
            fields = {
                'name': name,
                'head': descriptor.head,
                'pattern': descriptor.pattern,
                'tail': descriptor.tail,
                '__slots__': (),
                }
            # build it
            token = type(name, (cls.token,), fields)
            # add it to the pile
            tokens.append(token)

        # attribute adjustments
        # replace the descriptors with the new token classes
        for token in tokens: attributes[token.name] = token
        # add the list of tokens
        attributes["pyre_tokens"] = tokens

        # build the scanner class record
        scanner = super().__new__(cls, name, bases, attributes, **kwds)

        # initialize the collection of token patterns
        patterns = []
        # and the known token names
        names = set()
        # iterate over all ancestors to build the recognizer
        for base in scanner.__mro__:
            # for classes that are {Lexer} instances
            if isinstance(base, cls):
                # for every token
                for token in base.pyre_tokens:
                    # get the token name
                    name = token.name
                    # skip shadowed tokens
                    if name in names: continue
                    # get the token pattern
                    pattern = token.pattern
                    # skip tokens with no patterns
                    if not pattern: continue
                    # for the rest, get the remaining pattern parts
                    head = token.head
                    tail = token.tail
                    # assemble the regular expression
                    regex = '{}(?P<{}>{}){}'.format(head, name, pattern, tail)
                    # add it to the pattern pile
                    patterns.append(regex)
            # in any case, add all the local names to the known pile
            names.update(base.__dict__)
                    
        # attach the recognizer
        scanner.pyre_recognizer = re.compile('|'.join(patterns))
        # return the scanner record
        # print('  done')
        return scanner


# end of file 
