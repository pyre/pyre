# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Definitions for all the exceptions raised by this package
"""


from ..framework.exceptions import FrameworkError


class NodeError(FrameworkError):
    """
    Base class for pyre.algebraic errors. Useful as a catch-all
    """


class CircularReferenceError(NodeError):
    """
    Signal a circular reference in the evaluation graph
    """
    
    def __init__(self, node, path=(), **kwds):
        msg = "the evaluation graph has a cycle at {0.node}"
        super().__init__(description=msg, **kwds)
        self.node = node
        self.path = path
        return


class EvaluationError(NodeError):
    """
    Base class for node evaluation exceptions
    """

    def __init__(self, error, node=None, **kwds):
        msg = "evaluation error: {0.error}"
        super().__init__(description=msg, **kwds)
        self.node = node
        self.error = error
        return


class ExpressionError(NodeError):
    """
    Base class for expression errors; useful when trapping them as a category
    """


class EmptyExpressionError(ExpressionError):
    """
    Exception raised when the expression factory did not encounter any named references to
    other nodes
    """

    def __init__(self, formula, **kwds):
        msg = "while parsing {0.expression!r}: no references found"
        super().__init__(description=msg, **kwds)
        self.expression = formula
        return


class ExpressionSyntaxError(ExpressionError):
    """
    Exception raised when the python interpreter encounters a syntax error while compiling the
    expression
    """

    def __init__(self, formula, error, **kwds):
        msg = "while evaluating {0.expression!r}: {0.error}"
        super().__init__(description=msg, **kwds)
        self.expression = formula
        self.error = error
        return


class UnresolvedNodeError(NodeError):
    """
    Signal a value request from an unresolved node
    """

    def __init__(self, name, node=None, **kwds):
        msg = "node {0.name!r} is unresolved"
        super().__init__(description=msg, **kwds)
        self.name = name
        self.node = node
        return


# end of file 
