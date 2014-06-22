# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


class Token:
    """
    Base class for tokens, the atomic units of recognizable text in a stream
    """


    # constants; set at compile time
    name = '' # the name of the token
    head = '' # a pattern for text required for a match but not part of the lexeme
    tail = '' # a pattern for text required for a match but not part of the lexeme
    pattern = '' # the regular expression that extracts the lexeme


    # meta methods
    def __init__(self, lexeme='', locator=None, **kwds):
        super().__init__(**kwds)
        self.lexeme = lexeme
        self.locator = locator
        return


    def __len__(self):
        """
        Compute the length of the lexeme

        N.B.: this is not the same as the footprint of the token in the input stream, which
        includes the {head} and {tail} of the token
        """
        return len(self.lexeme)


    def __str__(self):
        """
        Textual representation, mostly for debugging purposes
        """
        # if there is a lexeme
        if self.lexeme:
            # render it along with the token name
            return "{{{0.name}: {0.lexeme!r}}}".format(self)
        # otherwise
        return "{{{0.name}}}".format(self)

    
    # implementation details
    __slots__ = (
        'lexeme', # the body of the token
        'locator', # marks the location of the lexeme in the input stream
        )
    

# end of file 
