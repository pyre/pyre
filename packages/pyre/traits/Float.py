# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
from .. import schemata
# superclass
from .Property import Property


# declaration
class Float(Property):
    """
    A property descriptor for floats
    """


    # public data
    default = 0
    schema = schemata.float


    # meta-methods
    def __init__(self, default=default, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file 
