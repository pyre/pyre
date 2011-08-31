# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Unary import Unary


class Opposite(Unary):
    """
    Compute the opposite of a node
    """


    def compute(self):
        """
        Compute and return my value
        """
        return -self._op.value


# end of file 
