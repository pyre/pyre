# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Expression import Expression


class Unary(Expression):
    """
    Base class for nodes that capture unary operations
    """


    def __init__(self, op, **kwds):
        super().__init__(**kwds)
        self.op = op
        return
    

# end of file 
