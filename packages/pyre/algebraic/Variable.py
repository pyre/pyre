# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Leaf import Leaf
from .Node import Node


class Variable(Leaf, Node):
    """
    Encapsulation of expression nodes that can hold a value.

    This is the main class exposed by this package.
    """


    # public data
    value = None


    # meta methods
    def __init__(self, value=None, **kwds):
        super().__init__(**kwds)
        self.value = value
        return


# end of file 
