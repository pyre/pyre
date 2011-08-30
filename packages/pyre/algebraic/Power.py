# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Binary import Binary


class Power(Binary):
    """
    A representation of raising one node to the power of the other
    """


    # public data
    symbol = "**" # a representation of my operation


    # interface
    def apply(self, op1, op2):
        # compute
        return op1 ** op2


# end of file 
