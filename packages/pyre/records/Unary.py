# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Derivation import Derivation


class Unary(Derivation):
    """
    Base class for derivation that capture unary operations
    """


    def __init__(self, op, **kwds):
        super().__init__(**kwds)
        self.op = op
        return
    

# end of file 
