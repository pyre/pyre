# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
from . import gsl # the extension


# the class declaration
class Vector:
    """
    A wrapper over a gsl vector
    """

    # initialization
    def zero(self):
        """
        Set all my elements to zero
        """
        # zero me out
        gsl.vector_set_zero(self.data)
        # and return
        return self


    # meta methods
    def __init__(self, size, **kwds):
        super().__init__(**kwds)
        self.size = size
        self.data = gsl.vector_allocate(size)
        return


    def __len__(self): return self.size


    # private data
    data = None


# end of file 
