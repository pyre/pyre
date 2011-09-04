# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Leaf:
    """
    Mix-in class that provides an implementation of the subset of the interface of {Node} that
    requires traversals of the expression graph rooted at leaf nodes.
    """


    # public data
    @property
    def variables(self):
        """
        Traverse my expression graph and return an iterable with all the variables I depend on

        Variables are reported as many times as they show up in my graph. Clients that are
        looking for the set unique dependencies have to prune the results themselves.
        """
        # just myself
        yield self
        # and no one else
        return


    # interface
    def validate(self, span=None, clean=None):
        """
        Make sure that the subgraph rooted at me is free of cycles

        parameters:
            {span}: the set of nodes previously visited; if i am in this set, there are cycles
            {clean}: the set of nodes known to be cycle free because they were previously cleared
        """
        # check whether i need to maintain the clean pile
        if clean is not None:
            # add myself to the clean set
            clean.add(self)
        # and return
        return self


    def substitute(self, replacements):
        """
        Replace variables in my graph that are present in {replacements} with the indicated node
        """
        # nothing to do
        return


# end of file 
