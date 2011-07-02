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


    # interface
    def pyre_eval(self, **kwds):
        # compute the value of the first operand
        op1 = self.op1.pyre_eval(**kwds)
        # compute the value of the second operand
        op2 = self.op2.pyre_eval(**kwds)
        # and put them together
        return op1 >= op2


    # meta methods
    def __str__(self):
        return "({0.op1} >= {0.op2})".format(self)


# end of file 
