# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# my ancestor
from .LineMill import LineMill


# my declaration
class Cxx(LineMill):
    """
    Support for C++
    """


    def __init__(self, **kwds):
        super().__init__(comment='//', languageMarker='-*- C++ -*-', **kwds)
        return


# end of file 
