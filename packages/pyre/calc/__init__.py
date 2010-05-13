# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
This package provides the implementation of a simple evaluation network.

There are two fundamental abstractions: nodes and evaluators. Nodes hold the values computed by
the evaluation network, and evaluators are operators attached to nodes that compute their
node's value by acting on the values of other nodes. These two abstractions provide the
machinery for representing arbitrary expressions as graphs.

The interesting aspect of this package is that nodal values get updated automatically when the
values of any of the nodes in their domain change. Nodes keep track of the set of evaluators
that are interested in their values and send notifications when their values change.

In addition, this package provides Model, a simple manager for evaluation nodes. Beyond node
storage, Model enables the naming of nodes and can act as the name resolution context for the
Expression evaluator, which evaluates strings with arbitrary python expressions that may
involve the values of nodes in the model. The other evaluators provided here operate
independently of Model. However, it is a good idea to build some kind of container to hold
nodes while the evaluation graph is in use.

Simple examples of the use of the ideas in this package are provided in the unit tests. For a
somewhat more advanced example, take a look at pyre.framework.Evaluator, which is a Model that
builds an evaluation network out of the traits of pyre components, so that trait settings can
refer to the values of other traits in the configuration files.
"""


# factories
# model
def newModel(*, name, **kwds):
    from .Model import Model
    return Model(name=name, **kwds)


# nodes
def newNode(value=None, **kwds):
    """
    Build a new node.

    parameters: 
        {value}: can be an Evaluator descendant, another Node, or any other python
                 object that will be interpreted as the literal value of the node
    """
    # build the node
    from .Node import Node
    from .Evaluator import Evaluator
    # inspect {value}
    # first, check whether we were passed an evaluator
    if isinstance(value, Evaluator):
        return Node(value=None, evaluator=value, **kwds)
    # perhaps {value} is another node
    if isinstance(value, Node):
        return value.newReference(**kwds)
    # otherwise, build a literal
    return Node(value=value, evaluator=None, **kwds)


# evaluators
def average(*args):
    """
    Create an evaluator that averages the values of the nodes in its domain
    """
    from .Average import Average
    return Average(domain=args)


def count(*args):
    """
    Create an evaluator that counts the number of nodes in its domain
    """
    from .Count import Count
    return Count(domain=args)


def expression(*, formula, model, **kwds):
    """
    Build a new expression evaluator, using {formula} as the python expression to evaluate, and
    {model} as the name resolution context
    """
    from .Expression import Expression
    return Expression(expression=formula, model=model, **kwds)


def max(*args):
    """
    Create an evaluator that computes the max of the values of the nodes in its domain
    """
    from .Maximum import Maximum
    return Maximum(domain=args)


def min(*args):
    """
    Create an evaluator that computes the min of the values of the nodes in its domain
    """
    from .Minimum import Minimum
    return Minimum(domain=args)


def product(*args):
    """
    Create an evaluator that computes the product of the values of the nodes in its domain
    """
    from .Product import Product
    return Product(domain=args)


def reference(node):
    """
    Create an evaluator that returns the value of the referent node
    """
    from .Reference import Reference
    return Reference(node=node)


def sum(*args):
    """
    Create an evaluator that sums the values of the nodes in its domain
    """
    from .Sum import Sum
    return Sum(domain=args)


# exceptions
from ..framework import FrameworkError


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

    def __init__(self, evaluator, error, formula, **kwds):
        super().__init__(evaluator, error, **kwds)
        self.expression = formula
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


# debugging support
_metaclass_Node = type
_metaclass_Evaluator = type

# end of file 
