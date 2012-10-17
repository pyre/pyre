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
class Object(Property):
    """
    A generic property descriptor
    """


    # public data
    default = None


    # framework support
    def macro(self, model):
        """
        Return my preferred macro converter
        """
        # do not build interpolations or expressions; just leave the value alone
        return model.variable


    # meta-methods
    def __init__(self, default=default, **kwds):
        # chain up
        super().__init__(schema=schema.object, default=default)
        # all done
        return


# end of file 
