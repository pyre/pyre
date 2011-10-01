# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Maximum:
    """
    The representation of the maximum value of a collection of nodes
    """


    # interface
    def getValue(self):
        """
        Compute and return my value
        """
        # compute and return my value 
        return max(operand.value for operand in self.operands)


# end of file 
