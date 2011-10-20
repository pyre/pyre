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


    # meta methods
    def __new__(cls, name, bases, attributes, tables=None, **kwds):
        # chain to my ancestor
        query = super().__new__(cls, name, bases, attributes, **kwds)

        # return the query class record
        return query


# end of file 
