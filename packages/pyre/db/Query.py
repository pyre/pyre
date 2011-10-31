# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# the metaclass
from .Selector import Selector


# declaration
class Query(metaclass=Selector, hidden=True):
    """
    Base class for describing database queries
    """


    # types
    pyre_Record = None


    # public data
    pyre_fields = ()
    pyre_tables = set()


# end of file 
