# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Binary import Binary


class Less(Binary):
    """
    A representation of less-than
    """


    # public data
    symbol = "<" # a representation of my operation


    # interface
    def apply(self, op1, op2):
        # compute
        return op1 < op2


# end of file 
