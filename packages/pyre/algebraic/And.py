# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Binary import Binary


class And(Binary):
    """
    Logical and
    """

    
    # public data
    symbol = "and" # a representation of my operation


    # interface
    def pyre_apply(self, op1, op2):
        # apply
        return op1 and op2


# end of file 
