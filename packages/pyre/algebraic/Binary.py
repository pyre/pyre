# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Node import Node


class Binary(Node):
    """
    Base class for nodes that capture binary operations
    """


    # meta methods
    def __init__(self, op1, op2, **kwds):
        super().__init__(**kwds)
        self.op1 = op1
        self.op2 = op2
        return
    

# end of file 
