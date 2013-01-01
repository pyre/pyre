# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


class Leaf:
    """
    Mix-in class that provides an implementation of the subset of the interface of {Node} that
    requires traversals of the expression graph rooted at leaf nodes.
    """


    # public data
    operands = () # leaves have no operands
    operators = () # leaves have no dependencies


    @property
    def span(self):
        """
        Traverse my subgraph and yield all its nodes
        """
        # just myself
        yield self
        # and no more
        return


    @property
    def variables(self):
        """
        Traverse my subgraph and return an iterable with all the variables in my graph

        Variables are reported as many times as they show up in my graph. Clients that are
        looking for the set unique dependencies have to prune the results themselves.
        """
        # just myself
        yield self
        # and no one else
        return


# end of file 
