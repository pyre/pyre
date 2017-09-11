# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2017 all rights reserved
#


class Composite:
    """
    Mix-in class that provides an implementation of the subset of the interface of {Node} that
    requires traversal of the expression graph rooted at nodes with dependencies.

    This class assumes that its instances provide {operands}, a tuple of their dependencies on
    other nodes
    """


    # types
    from .exceptions import CircularReferenceError


    # public data
    operands = ()


    # meta-methods
    def __init__(self, operands, **kwds):
        super().__init__(**kwds)
        self.operands = operands
        return


    # implementation details
    def _substitute(self, current, replacement):
        """
        Adjust the operands by substituting {replacement} for {current} in the sequence of operands
        """
        # save the locations that have to be modified
        indices = []
        # go through my operands
        for index, op in enumerate(self.operands):
            # check carefully for a match
            if op is current:
                # and add the index to the pile
                indices.append(index)
        # now that we have found them all
        for index in indices:
            # replace them
            self.operands[index] = replacement
        # all done
        return self


# end of file
