# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Node import Node


class Literal(Node):
    """
    Wrapper around foreign values that endows them with {Node} interface
    """


    # traversal of the nodes in my expression tree
    @property
    def pyre_dependencies(self):
        """
        Traverse my expression tree looking for leaf nodes
        """
        # literals don't count as true dependencies
        return []


    # interface
    def pyre_eval(self, **kwds):
        """
        Compute my value
        """
        # easy enough...
        return self.value


    # meta methods
    def __init__(self, value, **kwds):
        super().__init__(**kwds)
        self.value = value
        return


# end of file 
