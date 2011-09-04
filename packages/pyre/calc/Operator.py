# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Node import Node
from .Dependent import Dependent


class Operator(Dependent, Node):
    """
    Representation of nodes whose values depend on other nodes
    """


    # public data
    @property
    def value(self):
        """
        Compute and return my value
        """
        # if my cached value is invalid
        if self._value is None:
            # compute the values of my operands
            values = tuple(op.value for op in self._operands)
            # apply my operator and cache the result
            self._value = self._operator(*values)
        # return it
        return self._value


    # meta methods
    def __init__(self, operator, **kwds):
        super().__init__(**kwds)
        self._operator = operator
        return
        

    # private data
    _operator = None


# end of file 
