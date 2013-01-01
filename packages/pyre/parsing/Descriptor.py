# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class Descriptor:
    """
    Place holders for the token specifications

    Descriptors are harvested by {Lexer}, the metaclass of {Scanner} subclasses, and converted
    into subclasses of {Token}
    """

    # public data
    head = '' # a pattern for text required for a match that is not part of the lexeme
    tail = '' # a pattern for text required for a match that is not part of the lexeme
    pattern = '' # the regular expression that extracts the lexeme


    # meta methods
    def __init__(self, pattern='', head='', tail='', **kwds):
        super().__init__(**kwds)
        self.head = head
        self.tail = tail
        self.pattern = pattern
        return


    def __str__(self):
        return "{{head: '{}', pattern: '{}', tail: '{}'}}".format(
            self.head, self.pattern, self.tail)


# end of file 
