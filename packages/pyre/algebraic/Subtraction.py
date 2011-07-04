# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Binary import Binary


class Subtraction(Binary):
    """
    A representation of the difference of two operands
    """

    # a representation for my operation
    symbol = '-'


    # interface
    def pyre_apply(self, op1, op2):
        # add my two operands
        return op1 - op2


# end of file 
