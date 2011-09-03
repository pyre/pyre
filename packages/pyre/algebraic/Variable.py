# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Node import Node


class Variable(Node):
    """
    Encapsulation of expression nodes that can hold a value.

    This is the main class exposed by this package.
    """


    # public data
    value = None


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
    def substitute(self, replacements):
        """
        Replace variables in my graph that are present in {replacements} with the indicated node
        """
        # nothing to do
        return


    # meta methods
    def __init__(self, value=None, **kwds):
        super().__init__(**kwds)
        self.value = value
        return

# end of file 
