# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Binary import Binary


class Multiplication(Binary):
    """
    Evaluator that computes the product of two nodes
    """


    def compute(self):
        return self._op1.value * self._op2.value


# end of file 
