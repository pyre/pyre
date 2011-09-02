# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


from .Node import Node


class Operator(Node):
    """
    Base class for all nodes that capture operations

    This class is really just a marker in the class hierarchy that enables clients to
    distinguish between literal nodes and nodes that capture operations.
    """


    # public data
    operator = None
    operands = None


    # traversal of the nodes in my expression graph
    @property
    def dependencies(self):
        """
        Traverse my expression graph looking for leaf nodes
        """
        # traverse my operands
        for operand in self.operands:
            # and ask them for their dependencies
            for node in operand.dependencies:
                # return whatever it discovered
                yield node
        # and no more
        return


    # interface
    def eval(self, **kwds):
        values = (op.eval(**kwds) for op in self.operands)
        return self.operator(*values)


    def dfs(self, **kwds):
        """
        Traverse an expression graph in depth-first order
        """
        # traverse my operands
        for operand in self.operands:
            # and ask them for their dependencies
            for node in operand.dfs(**kwds):
                # return whatever it discovered
                yield node
        # now return myself
        yield self
        # and no more
        return


    def substitute(self, replacements):
        """
        Look through the dictionary {replacements} for any of my operands and replace them with
        the indicated nodes.
        """
        operands = []
        # look through my operands
        for operand in self.operands:
            # does this one show up in the replacement map?
            if operand in replacements:
                # push its replacement to the new operand list
                operands.append(replacements[operand])
            # otherwise
            else:
                # push it
                operands.append(operand)
                # and hand it the replacement list
                operand.substitute(replacements)
        # install the new operands
        self.operands = tuple(operands)
        # and return
        return
                    

    # meta methods
    def __init__(self, operator, operands, **kwds):
        super().__init__(**kwds)
        self.operator = operator
        self.operands = operands
        return


# end of file 
