# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the pyre package
import pyre
# my ancestor
from .LineMill import LineMill


# my declaration
class F90(LineMill):
    """
    Support for Fortran 90
    """


    # traits
    languageMarker = pyre.properties.str(default='F90')
    languageMarker.doc = "the variant to use in the language marker"

    
    # meta methods
    def __init__(self, **kwds):
        super().__init__(comment='!', **kwds)
        return


# end of file 
