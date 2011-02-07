# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .PseudoUnary import PseudoUnary


class LeftFloorDivision(PseudoUnary):
    """
    A representation of the integer ratio of two operands where the left operand is a Node
    and the right operand is a foreign value
    """


    # interface
    def eval(self, **kwds):
        # compute the value of my node operand
        op = self.op.eval(**kwds)
        # and put them together
        return op // self.value


    # meta methods
    def __str__(self):
        return "({0.op} // {0.value})".format(self)


# end of file 
