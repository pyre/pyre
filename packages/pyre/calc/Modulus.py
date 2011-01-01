# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Unary import Unary


class Modulus(Unary):
    """
    Scale the value of another node by a constant
    """


    def compute(self):
        """
        Compute and return my value
        """
        return abs(self._op.value)


# end of file 
