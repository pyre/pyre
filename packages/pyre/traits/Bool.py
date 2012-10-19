# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
from .. import schema
# superclass
from .Property import Property


# declaration
class Bool(Property):
    """
    A property that represents booleans
    """


    # public data
    default = True
    schema = schema.bool


    # meta-methods
    def __init__(self, default=default, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file 
