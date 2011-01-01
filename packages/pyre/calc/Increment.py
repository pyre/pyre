# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Unary import Unary


class Increment(Unary):
    """
    Scale the value of another node by a constant
    """


    def compute(self):
        """
        Compute and return my value
        """
        return self._increment + self._op.value


    # meta-methods
    def __init__(self, increment, **kwds):
        super().__init__(**kwds)
        self._increment = increment
        return


# end of file 
