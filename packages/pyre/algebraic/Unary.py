# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Expression import Expression


class Unary(Expression):
    """
    Base class for nodes that capture unary operations
    """


    # traversal of the nodes in my expression tree
    @property
    def pyre_dependencies(self):
        """
        Traverse my expression tree looking for leaf nodes
        """
        # traverse my expression
        for node in self.op.pyre_dependencies:
            # and yield any nodes discovered
            yield node
        # all done
        return


    # meta methods
    def __init__(self, op, **kwds):
        super().__init__(**kwds)
        self.op = op
        return
    

# end of file 
