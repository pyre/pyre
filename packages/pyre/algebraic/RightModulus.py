# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .PseudoUnary import PseudoUnary


class RightModulus(PseudoUnary):
    """
    A representation of the integer ratio of two operands where the left operand is a foreign
    value while the right operand is a Node
    """


    # interface
    def eval(self, **kwds):
        # compute the value of my node operand
        op = self.op.eval(**kwds)
        # and put them together
        return self.value % op


    # meta methods
    def __str__(self):
        return "({0.value} % {0.op})".format(self)


# end of file 
