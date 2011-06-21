# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# the base class that triggers descriptor sniffing
from ..patterns.AttributeClassifier import AttributeClassifier


# declaration
class Schemer(AttributeClassifier):
    """
    Metaclass that inspects a table declaration and builds the information necessary to connect
    its attributes to the columns of the underlying table in the database back end
    """


    # meta methods
    def __new__(cls, name, bases, attributes, **kwds):
        # chain to the ancestors
        table = super().__new__(cls, name, bases, attributes, **kwds)
        # all done
        return table


    def __init__(self, name, bases, attributes, **kwds):
        # chain to the ancestors
        super().__init__(name, bases, attributes, **kwds)
        # all done
        return


# end of file 
