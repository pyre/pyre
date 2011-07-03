# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Binary import Binary


class Or(Binary):
    """
    Logical or
    """


    # public data
    symbol = "or" # a representation of my operation


    # interface
    def pyre_apply(self, op1, op2):
        # compute
        return op1 or op2


# end of file 
