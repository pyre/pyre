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


    # meta-methods
    def __init__(self, default=default, **kwds):
        # chain up
        super().__init__(schema=schema.bool, default=default)
        # all done
        return


# end of file 
