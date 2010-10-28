# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Binary import Binary


class Division(Binary):
    """
    A representation of the ratio of two operands
    """


    # interface
    def eval(self, values, index):
        # compute the value of the first operand
        try:
            op1 = self.op1.eval(values=values, index=index)
        except AttributeError:
            op1 = self.op1
        # compute the value of the second operand
        try:
            op2 = self.op2.eval(values=values, index=index)
        except AttributeError:
            op2 = self.op2
        # and put them together
        return op1 / op2


# end of file 
