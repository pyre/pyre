# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
from ..schema import tuple
# superclass
from .Property import Property


# declaration
class Tuple(Property):
    """
    A property that represents tuples
    """


    # public data
    default = ()
    schema = tuple(schema=tuple.identity)


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
        # save my schema
        self.schema = schema.tuple(schema=schema)
        # all done
        return


# end of file 
