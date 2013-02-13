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
class Object(Property):
    """
    A generic property descriptor
    """


    # public data
    default = None
    schema = schemata.identity


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
        super().__init__(default=default, **kwds)
        # all done
        return


# end of file 
