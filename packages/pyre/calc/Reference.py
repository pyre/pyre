# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Node import Node
from .Dependent import Dependent


class Reference(Dependent, Node):
    """
    A node that refers to another node
    """

    # public data
    @property
    def value(self):
        """
        Compute and return my value
        """
        # if my cached value is invalid
        if self._value is None:
            # get my referent
            referent, = self.operands
            # update my cache
            self._value = referent.value
        # return my value
        return self._value


    # meta methods
    def __init__(self, node, **kwds):
        super().__init__(operands=(node,), **kwds)
        # all done
        return


# end of file 
