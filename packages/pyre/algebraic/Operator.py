# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Operator:
    """
    Mix-in class that forms the basis of the representation of operations among nodes
    """


    # public data
    evaluator = None
    operands = None

    @property
    def value(self):
        """
        Compute and return my value
        """
        # compute the values of my operands
        values = tuple(op.value for op in self.operands)
        # apply my operator
        return self.evaluator(*values)


    # meta methods
    def __init__(self, evaluator, operands, **kwds):
        super().__init__(**kwds)
        self.evaluator = evaluator
        self.operands = operands
        return


# end of file 
