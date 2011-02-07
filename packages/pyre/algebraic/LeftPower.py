# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .PseudoUnary import PseudoUnary


class LeftPower(PseudoUnary):
    """
    A representation of exponentiation, assuming that the base is a Node while the exponent is
    a foreign value
    """


    # interface
    def eval(self, **kwds):
        # compute the value of my node operand
        op = self.op.eval(**kwds)
        # and raise the foreign value to this power
        return op ** self.value


    # meta methods
    def __str__(self):
        return "({0.op} ** {0.value})".format(self)


# end of file 
