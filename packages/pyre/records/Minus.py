# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Unary import Unary


class Minus(Unary):
    """
    A representation of unary minus
    """


    # interface
    def eval(self, values, index):
        # compute the value of my operand
        try:
            op = self.op.eval(values=values, index=index)
        except AttributeError:
            op = self.op
        # compute
        return -op


    # meta methods
    def __str__(self):
        return "(-{0.op})".format(self)


# end of file 
