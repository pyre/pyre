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
        super().__init__(**kwds)
        self.node = node
        self.path = path
        return

    def __str__(self):
        return "the evaluation graph has a cycle at {0.node}".format(self)


class DuplicateNodeError(NodeError):
    """
    Exception raised when an attempt is made to insert a node and the model already
    contains a node by the same name
    """

    def __init__(self, model, name, node, **kwds):
        super().__init__(**kwds)
        self.model = model
        self.name = name
        self.node = node
        return

    def __str__(self):
        return "model {0.model!r}: duplicate name {0.name!r}".format(self)

        
class EvaluationError(NodeError):
    """
    Base class for node evaluation exceptions
    """

    def __init__(self, evaluator, error, **kwds):
        super().__init__(**kwds)
        self.evaluator = evaluator
        self.error = error
        return

    def __str__(self):
        return "evaluation error: {0.error}".format(self)


class ExpressionError(EvaluationError):
    """
    Exception raised when the python interpreter encounters a SyntaxError compiling the
    expression
    """

    def __init__(self, evaluator, **kwds):
        super().__init__(evaluator, **kwds)
        self.expression = evaluator._formula
        self.program = evaluator._program
        return

    def __str__(self):
        return "while evaluating {0.expression!r}: {0.error}".format(self)


class UnresolvedNodeError(NodeError):
    """
    Signal a value request from an unresolved node
    """

    def __init__(self, name, node, **kwds):
        super().__init__(**kwds)
        self.name = name
        self.node = node
        return

    def __str__(self):
        return "node {0.name!r} is unresolved".format(self)


# end of file 
