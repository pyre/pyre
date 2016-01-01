# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2016 all rights reserved
#


class Sequence:
    """
    Mix-in class that forms the basis of the representation of sequences
    """


    # interface
    def getValue(self, **kwds):
        """
        Compute and return my value
        """
        # return the value of each operand
        return (op.value for op in self.operands)


# end of file
