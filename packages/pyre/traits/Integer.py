# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
from .. import schema
# superclass
from .Property import Property


# declaration
class Integer(Property):
    """
    A property descriptor for integers
    """


    # public data
    default = 0
    schema = schema.int


    # meta-methods
    def __init__(self, default=default, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file 
