# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


class TokenDescriptor(object):
    """
    Class whose instances holds the token declaration information until the Lexer is able to
    build the actual token class
    """


    # public data
    name = None
    pattern = None


    # meta methods
    def __init__(self, pattern, **kwds):
        super().__init__(**kwds)
        self.pattern = pattern
        return


    # meta data
    _pyre_category = "tokens" # for the AttributeClassifier


# end of file 
