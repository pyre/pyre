# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Unary import Unary


class ScalarPower(Unary):
    """
    Raise the value of a node to an exponent
    """


    def compute(self):
        """
        Compute and return my value
        """
        return self._op.value ** self._exponent 


    # meta-methods
    def __init__(self, exponent, **kwds):
        super().__init__(**kwds)
        self._exponent = exponent
        return


# end of file 
