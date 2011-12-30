# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# access to the pyre package
import pyre
# my ancestor
from .LineMill import LineMill


# my declaration
class Make(LineMill):
    """
    Support for makefiles
    """


    # traits
    languageMarker = pyre.properties.str(default='Makefile')
    languageMarker.doc = "the language marker"

    
    # meta methods
    def __init__(self, **kwds):
        super().__init__(comment='#', **kwds)
        return


# end of file 
