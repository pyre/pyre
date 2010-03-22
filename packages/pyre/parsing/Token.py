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


    # meta methods
    def __init__(self, lexeme, **kwds):
        super().__init__(**kwds)
        self.lexeme = lexeme
        return


    def __len__(self):
        return len(self.lexeme)


    def __str__(self):
        return "\{token: {0.lexeme!r}\}".format(self)


    # narrow the footprint down a bit
    __slots__ == ("lexeme",)


# end of file 
