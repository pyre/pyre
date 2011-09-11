# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Node import Node
from .Dependent import Dependent


class Average(Dependent, Node):
    """
    The representation of the average value of nodes
    """


    # public data
    @property
    def value(self):
        """
        Compute and return my value
        """
        # if my cached value is invalid
        if self._value is None:
            # evaluate my operands
            values = tuple(operand.value for operand in self.operands)
            # compute the average
            self._value = sum(values)/len(values)
        # and return it
        return self._value


# end of file 
