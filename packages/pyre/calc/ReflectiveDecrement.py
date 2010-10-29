# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Unary import Unary


class ReflectiveDecrement(Unary):
    """
    Subtract the value of a node from a scalar; useful for __rsub__ implementations
    """


    def compute(self):
        """
        Compute and return my value
        """
        return self._increment - self._op.value


    # meta-methods
    def __init__(self, increment, **kwds):
        super().__init__(**kwds)
        self._increment = increment
        return


# end of file 
