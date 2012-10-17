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
class String(Property):
    """
    A property that represents strings
    """


    # public data
    default = ''


    # framework support
    def macro(self, model):
        """
        Return my preferred macro processor
        """
        # build interpolations
        return model.interpolation


    # meta-methods
    def __init__(self, default=default, **kwds):
        # chain up
        super().__init__(schema=schema.str, default=default)
        # all done
        return


# end of file 
