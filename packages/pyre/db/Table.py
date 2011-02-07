# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# metaclass
from .Schemer import Schemer


# declaration
class Table(metaclass=Schemer):
    """
    Base class for database table declarations
    """


    # meta methods
    def __init__(self, **kwds):
        # chain to the ancestors
        super().__init__(**kwds)
        # all done
        return


# end of file 
