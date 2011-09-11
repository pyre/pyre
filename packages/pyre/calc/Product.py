# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import operator
import functools

from .Node import Node
from .Dependent import Dependent


class Product(Dependent, Node):
    """
    The representation of the product of nodes
    """


    # public data
    @property
    def value(self):
        """
        Compute and return my value
        """
        # if my cached value is invalid
        if self._value is None:
            # compute it
            self._value = functools.reduce(operator.mul, (op.value for op in self.operands))
        # and return it
        return self._value


# end of file 
