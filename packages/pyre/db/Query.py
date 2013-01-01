# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
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
    where = None # retrieve only rows that satisfy this expression
    order = None # control over the sorting order of the results
    group = None # aggregate the results using the distinct values of this column

    # metaclass decorations; treat as read-only
    # locally declared
    pyre_localFields = ()
    pyre_localDescriptors = {}
    # the complete set
    pyre_fields = () # the query fields
    pyre_tables = set() # the set of tables referenced by the query


# end of file 
