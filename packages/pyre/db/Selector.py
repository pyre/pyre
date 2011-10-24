# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# the base class that triggers descriptor sniffing
from ..patterns.AttributeClassifier import AttributeClassifier


# declaration
class Selector(AttributeClassifier):
    """
    Metaclass that inspects a query declaration and collects the information necessary to build
    the corresponding SELECT expressions
    """


    # types
    from .ColumnReference import ColumnReference


    # meta methods
    def __new__(cls, name, bases, attributes, table=None, hidden=False, **kwds):
        # chain to my ancestor
        query = super().__new__(cls, name, bases, attributes, **kwds)
        # leave early if this is a pyre internal class
        if hidden: return query

        # attach the meta data
        query.pyre_table = table

        # extract the column references
        query.pyre_columns = tuple(cls.pyre_harvest(attributes, cls.ColumnReference))

        # return the query class record
        return query


# end of file 
