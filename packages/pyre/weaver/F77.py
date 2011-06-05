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
class F77(LineMill):
    """
    Support for Fortran 77
    """


    # traits
    languageMarker = pyre.properties.str(default='Fortran')
    languageMarker.doc = "the variant to use in the language marker"

    
    # meta methods
    def __init__(self, **kwds):
        super().__init__(comment='c', **kwds)
        return


# end of file 
