# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


class Evaluator:
    """
    Mix-in class that computes the value of operator nodes by invoking their evaluator on their
    operands
    """


    # interface
    def getValue(self, **kwds):
        """
        Compute and return my value
        """
        # compute the values of my operands
        values = tuple(op.value for op in self.operands)
        # apply my operator
        return self.evaluator(*values)


# end of file 
