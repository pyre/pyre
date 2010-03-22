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
    regexp = None


    # meta data
    _pyre_category = "tokens" # for the AttributeClassifier


    # meta methods
    def __init__(self, regexp, **kwds):
        super().__init__(**kwds)
        self.regexp = regexp
        return


# end of file 
