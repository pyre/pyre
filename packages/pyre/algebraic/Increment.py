# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .PseudoUnary import PseudoUnary


class Increment(PseudoUnary):
    """
    Representation of incrementing a node by a foreign value
    """


    # interface
    def eval(self, **kwds):
        # compute the value of the operand
        op = self.op.eval(**kwds)
        # and increment it
        return op + self.value


    # meta methods
    def __str__(self):
        return "({0.op} + {0.value})".format(self)


# end of file 
