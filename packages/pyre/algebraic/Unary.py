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


    # interface
    def pyre_patch(self, replacements):
        """
        Look through the dictionary {replacements} for any of my operands and replace them with
        the indicated nodes.
        """
        # check whether my operand shows in the map
        if self.op in replacements:
            # it does; replace it
            self.op = replacements[self.op]
        # otherwise
        else:
            # pass the replacement map down
            self.op.pyre_patch(replacements)
        # all done
        return


    def pyre_eval(self, **kwds):
        """
        Evaluate my operand and then apply the operation i represent
        """
        # compute the value of my operand
        op = self.op.pyre_eval(**kwds)
        # and compute
        return self.pyre_apply(op)


    # meta methods
    def __init__(self, op, **kwds):
        super().__init__(**kwds)
        self.op = op
        return
    

# end of file 
