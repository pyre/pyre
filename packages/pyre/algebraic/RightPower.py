# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .PseudoUnary import PseudoUnary


class RightPower(PseudoUnary):
    """
    A representation of exponentiation where the base is a foreign value and the exponent is a
    Node
    """


    # interface
    def eval(self, **kwds):
        # compute the value of my node operand
        op = self.op.eval(**kwds)
        # and put them together
        return self.value ** op


    # meta methods
    def __str__(self):
        return "({0.value} ** {0.op})".format(self)


# end of file 
