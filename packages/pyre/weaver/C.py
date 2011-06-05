# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# my ancestor
from .BlockMill import BlockMill


# my declaration
class C(BlockMill):
    """
    Support for C
    """


    def __init__(self, **kwds):
        super().__init__(
            startBlock='/*', commentMarker=' * ', endBlock=' */',
            languageMarker='-*- C -*-', **kwds)
        return


# end of file 
