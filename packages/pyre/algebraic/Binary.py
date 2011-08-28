# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Operator import Operator


class Binary(Operator):
    """
    Base class for nodes that capture binary operations
    """


    # traversal of the nodes in my expression graph
    @property
    def pyre_dependencies(self):
        """
        Traverse my expression graph looking for leaf nodes
        """
        # visit my left operand
        for node in self.op1.pyre_dependencies:
            # yield any nodes discovered
            yield node
        # and now my right operand
        for node in self.op2.pyre_dependencies:
            # yield any nodes discovered
            yield node
        # all done
        return


    # interface
    def pyre_patch(self, replacements):
        """
        Look through the dictionary {replacements} for any of my operands and replace them with
        the indicated nodes.
        """
        # check whether my left operand shows in the map
        if self.op1 in replacements:
            # it does; replace it
            self.op1 = replacements[self.op1]
        # otherwise
        else:
            # pass the replacement map down
            self.op1.pyre_patch(replacements)

        # check whether my right operand shows in the map
        if self.op2 in replacements:
            # it does; replace it
            self.op2 = replacements[self.op2]
        # otherwise
        else:
            # pass the replacement map down
            self.op2.pyre_patch(replacements)
        # all done
        return


    def pyre_eval(self, **kwds):
        """
        Evaluate my two operands and then apply the operation i represent
        """
        # compute the value of the first operand
        op1 = self.op1.pyre_eval(**kwds)
        # compute the value of the second operand
        op2 = self.op2.pyre_eval(**kwds)
        # and put them together
        return self.pyre_apply(op1, op2)


    def pyre_dfs(self, **kwds):
        """
        Traverse an expression graph in depth-first order
        """
        # traverse my left operand
        for node in self.op1.pyre_dfs(**kwds):
            # return whatever it discovered
            yield node
        # repeat for my right operand
        for node in self.op2.pyre_dfs(**kwds):
            # and return whatever it discovered
            yield node
        # now return myself
        yield self
        # and no more
        return


    # meta methods
    def __init__(self, op1, op2, **kwds):
        super().__init__(**kwds)
        self.op1 = op1
        self.op2 = op2
        return


    # meta methods
    def __str__(self):
        return "({0.op1} {0.symbol} {0.op2})".format(self)
    

# end of file 
