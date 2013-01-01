# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# metaclass
from .Schemer import Schemer


# declaration
class View(metaclass=Schemer):
    """
    Base class for read-only accesses to the information in a data store
    """


    # meta methods
    def __init__(self, **kwds):
        # chain to the ancestors
        super().__init__(**kwds)
        # all done
        return


# end of file 
