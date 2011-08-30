# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Binary import Binary


class Division(Binary):
    """
    A representation of division among two nodes
    """


    # public data
    symbol = "/" # a representation for my operation


    # interface
    def apply(self, op1, op2):
        # apply
        return op1 / op2


# end of file 
