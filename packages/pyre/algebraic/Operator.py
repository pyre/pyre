# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Node import Node
from .Composite import Composite


class Operator(Composite, Node):
    """
    Representation of operations among nodes
    """


    # public data
    @property
    def value(self):
        """
        Compute and return my value
        """
        # compute the values of my operands
        values = tuple(op.value for op in self._operands)
        # apply my operator
        return self._operator(*values)


    # meta methods
    def __init__(self, operator, operands, **kwds):
        super().__init__(**kwds)
        self._operator = operator
        self._operands = operands
        return


    # private data
    _operator = None
    _operands = None


# end of file 
