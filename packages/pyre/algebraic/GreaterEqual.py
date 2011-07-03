# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Binary import Binary


class GreaterEqual(Binary):
    """
    A representation of greater-than-or-equal-to
    """


    # public data
    symbol = ">=" # a representation for my operation


    # interface
    def pyre_apply(self, op1, op2):
        # compute
        return op1 >= op2


# end of file 
