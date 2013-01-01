# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
from ..schema import list
# superclass
from .Property import Property


# declaration
class List(Property):
    """
    A property that represents lists
    """


    # public data
    default = []
    schema = list(schema=list.identity)


    # framework support
    def macro(self, model):
        """
        Return my preferred macro processor
        """
        # ask my schema
        return self.schema.macro(model=model)


    # meta-methods
    def __init__(self, schema=schema, default=default, **kwds):
        # chain up
        super().__init__(default=default, **kwds)
        # record my schema
        self.schema = list(schema=schema)
        # all done
        return


# end of file 
