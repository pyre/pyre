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
class INet(Property):
    """
    A property that represents internet addresses
    """


    # public data
    default = schema.inet.any


    # framework support
    def macro(self, model):
        """
        Return my preferred macro converter
        """
        # build interpolations
        return model.interpolation


    # meta-methods
    def __init__(self, default=default, **kwds):
        # chain up
        super().__init__(schema=schema.inet, default=default)
        # all done
        return


# end of file 
