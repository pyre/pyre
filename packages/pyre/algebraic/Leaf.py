# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


class Leaf:
    """
    Mix-in class that provides an implementation of the subset of the interface of {Node} that
    requires traversals of the expression graph rooted at leaf nodes.
    """


    # interface
    @property
    def span(self):
        """
        Traverse my subgraph and yield all its nodes
        """
        # just myself
        yield self
        # and nothing else
        return


    # structural classifiers
    @property
    def leaves(self):
        """
        Return a sequence over the leaves in my dependency graph
        """
        # i am one
        yield self
        # all done
        return


    # implementation details
    def _substitute(self, current, replacement, clean):
        """
        The node substitution workhorse
        """
        # if i'm the one being replaced
        if current is self:
            # return {replacement} and a marker that a substitution was performed
            return replacement
        # otherwise, add me to the clean pile
        clean.add(self)
        # and make sure they leave me alone
        return self


# end of file
