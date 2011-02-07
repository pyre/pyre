# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .PseudoUnary import PseudoUnary


class LeftModulus(PseudoUnary):
    """
    A representation of the remainder from the division of two operands. This one assumes that
    the first operand is a Node while the second is a foreign value
    """


    # interface
    def eval(self, **kwds):
        # compute the value of my node operand
        op = self.op.eval(**kwds)
        # and put them together
        return op % self.value


    # meta methods
    def __str__(self):
        return "({0.op} % {0.value})".format(self)


# end of file 
