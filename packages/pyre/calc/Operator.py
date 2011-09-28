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
    Encapsulation of the algebraic operations among nodes
    """


    # public data
    evaluator = None


    @property
    def value(self):
        """
        Compute and return my value
        """
        # if my cached value is invalid
        if self._value is None:
            # compute the values of my operands
            values = tuple(op.value for op in self.operands)
            # apply my operator and cache the result
            self._value = self.evaluator(*values)
        # return it
        return self._value


    # meta methods
    def __init__(self, evaluator, **kwds):
        super().__init__(**kwds)
        self.evaluator = evaluator
        return


# end of file 
