# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class Operator:
    """
    Mix-in class that forms the basis of the representation of operations among nodes
    """


    # constants
    category = 'operator'


    # public data
    evaluator = None


    # interface
    def getValue(self):
        """
        Compute and return my value
        """
        # compute the values of my operands
        values = (op.value for op in self.operands)
        # apply my operator
        return self.evaluator(*values)


    # meta-methods
    def __init__(self, evaluator, **kwds):
        super().__init__(**kwds)
        self.evaluator = evaluator
        return


# end of file 
