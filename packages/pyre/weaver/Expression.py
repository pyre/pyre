# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


class Expression:
    """
    This mill mix-in builds textual representations of expression trees built out of
    {pyre.algebraic.Node} subclasses
    """


    # types
    from . import algebraic


    # interface
    def expression(self, root, **kwds):
        """
        Build a representation of {node}, assumed to be an instance of a {pyre.algebraic.Node}
        subclass
        """
        return self._renderers[root.__class__](root, **kwds)


    # meta methods
    def __init__(self, **kwds):
        super().__init__(**kwds)

        self._symbols = self._newSymbolTable()
        self._renderers = self._newRenderingStrategyTable()

        return


    # implementation details
    def _newSymbolTable(self):
        """
        Build a table mapping all {pyre.algebraic} operators to their 'default' symbols

        This table is built by considering the python representation of the operator to be its
        default. Other mills can build their own tables, or start with this one and modify it as
        needed
        """
        # build the symbol table
        symbols = {
            self.algebraic.Addition: "+",
            self.algebraic.And: "and",
            self.algebraic.Division: "/",
            self.algebraic.Equal: "==",
            self.algebraic.FloorDivision: "//",
            self.algebraic.Greater: ">",
            self.algebraic.GreaterEqual: ">=",
            self.algebraic.Less: "<",
            self.algebraic.LessEqual: "<=",
            self.algebraic.Modulus: "%",
            self.algebraic.Multiplication: "*",
            self.algebraic.NotEqual: "!=",
            self.algebraic.Or: "or",
            self.algebraic.Power: "**",
            self.algebraic.Subtraction: "-",
            }
        # and return it
        return symbols


    def _newRenderingStrategyTable(self):
        """
        Build a table that maps {pyre.algebraic} operators to rendering strategies
        """
        # build the symbol table
        handlers = {
            # nodes
            self.algebraic.Node: self._literalRenderer,
            self.algebraic.Literal: self._literalRenderer,

            # unary operators
            self.algebraic.Absolute: self._absoluteRenderer,
            self.algebraic.Opposite: self._oppositeRenderer,

            # binary operators
            self.algebraic.Addition: self._binaryOperatorRenderer,
            self.algebraic.And: self._binaryOperatorRenderer,
            self.algebraic.Division: self._binaryOperatorRenderer,
            self.algebraic.Equal: self._binaryOperatorRenderer,
            self.algebraic.FloorDivision: self._binaryOperatorRenderer,
            self.algebraic.Greater: self._binaryOperatorRenderer,
            self.algebraic.GreaterEqual: self._binaryOperatorRenderer,
            self.algebraic.Less: self._binaryOperatorRenderer,
            self.algebraic.LessEqual: self._binaryOperatorRenderer,
            self.algebraic.Modulus: self._binaryOperatorRenderer,
            self.algebraic.Multiplication: self._binaryOperatorRenderer,
            self.algebraic.NotEqual: self._binaryOperatorRenderer,
            self.algebraic.Or: self._binaryOperatorRenderer,
            self.algebraic.Power: self._binaryOperatorRenderer,
            self.algebraic.Subtraction: self._binaryOperatorRenderer,
            }

        # and return it
        return handlers


    # the actual rendering strategies
    def _absoluteRenderer(self, node, **kwds):
        """
        Render the absolute value of {node}
        """
        # render my operand
        op = self._renderers[node.op.__class__](node=node.op)
        # and return my string
        return "abs({})".format(op)
        

    def _inverseRenderer(self, node, **kwds):
        """
        Render the inverse of {node}
        """
        # render my operand
        op = self._renderers[node.op.__class__](node=node.op)
        # and return my string
        return "(1/{})".format(op)
        

    def _oppositeRenderer(self, node, **kwds):
        """
        Render the opposite of {node}
        """
        # render my operand
        op = self._renderers[node.op.__class__](node=node.op)
        # and return my string
        return "(-{})".format(op)
        

    def _absoluteRenderer(self, node, **kwds):
        """
        Render the absolute value of {node}
        """
        # render my operand
        op = self._renderers[node.op.__class__](node=node.op)
        # and return my string
        return "abs({})".format(op)
        

    def _literalRenderer(self, node, **kwds):
        """
        Render {node} as a literal
        """
        # return the literal representation
        return str(node)


    def _binaryOperatorRenderer(self, node, **kwds):
        """
        Render {node} assuming it is a binary operator
        """
        # render the left operand
        op1 = self._renderers[node.op1.__class__](node=node.op1, **kwds)
        # render the right operand
        op2 = self._renderers[node.op2.__class__](node=node.op2, **kwds)
        # look up the operator symbol
        symbol = self._symbols[node.__class__]
        # put it all together
        return "({} {} {})".format(op1, symbol, op2)


# end of file 
