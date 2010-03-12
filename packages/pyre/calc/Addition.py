# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


from .Binary import Binary


class Addition(Binary):
    """
    Evaluator that computes the sum of two nodes
    """


    def compute(self):
        return self._op1.value + self._op2.value


# end of file 
