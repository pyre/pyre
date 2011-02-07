# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Unary import Unary


class Opposite(Unary):
    """
    A representation of unary minus
    """


    # interface
    def eval(self, **kwds):
        # compute the value of my operand
        op = self.op.eval(**kwds)
        # reverse its sign and return it
        return -op


    # meta methods
    def __str__(self):
        return "(-{0.op})".format(self)


# end of file 
