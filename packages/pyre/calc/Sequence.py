# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


class Sequence:
    """
    Mix-in class that forms the basis of the representation of sequences
    """


    # classifiers
    @property
    def sequences(self):
        """
        Return a sequence over sequences in my dependency graph
        """
        # i am one
        yield self
        # nothing further
        return


    # interface
    def getValue(self, **kwds):
        """
        Compute and return my value
        """
        # return the value of each operand
        return (op.value for op in self.operands)


# end of file
