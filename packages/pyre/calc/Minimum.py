# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Node import Node
from .Dependent import Dependent


class Minimum(Dependent, Node):
    """
    The representation of the minimum value of a collection of nodes
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
            self._value = min(operand.value for operand in self._operands)
        # and return it
        return self._value


# end of file 
