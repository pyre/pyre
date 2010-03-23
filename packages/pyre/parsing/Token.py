# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class Token(object):
    """
    Base class for tokens, the atomic units of recognizable text in a stream
    """


    # constants
    pattern = None
    recognizer = None


    # meta methods
    def __init__(self, *, lexeme="", locator=None, **kwds):
        super().__init__(**kwds)
        self.lexeme = lexeme
        self.locator = locator
        return


    def __len__(self):
        return len(self.lexeme)


    def __str__(self):
        # if there is a lexeme, print it
        if self.lexeme:
            return "{{{0.__class__.__name__}: {0.lexeme!r}}}".format(self)
        # otherwise, just note the token class
        return "{{{0.__class__.__name__}}}".format(self)


    # narrow down the footprint a bit
    __slots__ = ("lexeme", "locator")


# end of file 
