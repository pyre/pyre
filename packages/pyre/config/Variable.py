# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from ..calc.Node import Node


class Variable(Node):
    """
    The object used to hold the values of all configurable items
    """


    # public data
    priority = (-1,-1)


    # meta methods
    def __init__(self, priority=priority, **kwds):
        super().__init__(**kwds)
        self.priority = priority
        return


# end of file 
