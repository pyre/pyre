# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
This package provides support for writing simple parsers
"""


# factories
def token(regexp=None):
    """
    Build a TokenDescriptor instance to hold the regeular expression until the Lexer has had a
    chance to process it and convert it into a class derived from Token
    """
    from .TokenDescriptor import TokenDescriptor
    return TokenDescriptor(regexp)


# end of file 
