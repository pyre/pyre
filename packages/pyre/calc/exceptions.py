# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Definitions for all the exceptions raised by this package
"""


from ..framework.exceptions import FrameworkError


class NodeError(FrameworkError):
    """
    Base class for pyre.calc errors. Useful as a catch-all
    """


class CircularReferenceError(NodeError):
    """
    Signal a circular reference in the evaluation graph
    """
    
    def __init__(self, node, path, **kwds):
        msg = "the evaluation graph has a cycle at {}".format(node)
        super().__init__(description=msg, **kwds)
        self.node = node
        self.path = path
        return


class DuplicateNodeError(NodeError):
    """
    Exception raised when an attempt is made to insert a node and the model already
    contains a node by the same name
    """

    def __init__(self, model, name, node, **kwds):
        msg = "model {!r}: duplicate name {!r}".format(model, name)
        super().__init__(description=msg, **kwds)
        self.model = model
        self.name = name
        self.node = node
        return

        
class EvaluationError(NodeError):
    """
    Base class for node evaluation exceptions
    """

    def __init__(self, evaluator, error, **kwds):
        msg = "evaluation error: {}".format(error)
        super().__init__(description=msg, **kwds)
        self.evaluator = evaluator
        self.error = error
        return


class EmptyExpressionError(NodeError):
    """
    Exception raised when the expression factory did not encounter any named references to
    other nodes
    """

    def __init__(self, formula, **kwds):
        msg = "while parsing {!r}: no references found".format(formula)
        super().__init__(description=msg, **kwds)
        self.expression = formula
        return


class ExpressionError(NodeError):
    """
    Exception raised when the python interpreter encounters a syntax error while compiling the
    expression
    """

    def __init__(self, formula, error, **kwds):
        msg = "while evaluating {!r}: {}".format(formula, error)
        super().__init__(description=msg, **kwds)
        self.expression = formula
        self.error = error
        return


class UnresolvedNodeError(NodeError):
    """
    Signal a value request from an unresolved node
    """

    def __init__(self, name, node, **kwds):
        msg = "node {!r} is unresolved".format(name)
        super().__init__(description=msg, **kwds)
        self.name = name
        self.node = node
        return


# end of file 
