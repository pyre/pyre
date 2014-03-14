# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2014 all rights reserved
#


"""
Definitions for all the exceptions raised by this package
"""


# pull the exceptions from {algebraic}
from ..algebraic.exceptions import NodeError, CircularReferenceError

# the local ones
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


class AliasingError(NodeError):
    """
    Signal that an alias was requested among names that were associated with existing nodes
    """

    def __init__(self, key, target, alias, targetNode, targetInfo, aliasNode, aliasInfo, **kwds):
        # build the error format string
        msg = "both {0.target!r} and {0.alias!r} have existing nodes"
        # chain up
        super().__init__(description=msg, **kwds)
        # save the information
        self.key = key
        self.target = target
        self.alias = alias
        self.targetNode = targetNode
        self.targetInfo = targetInfo
        self.aliasNode = aliasNode
        self.aliasInfo = aliasInfo
        # all done
        return


# end of file 
