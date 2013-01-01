# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class Sum:
    """
    The representation of the sum of nodes
    """

    # interface
    def getValue(self):
        """
        Compute and return my value
        """
        return sum(operand.value for operand in self.operands)


# end of file 
