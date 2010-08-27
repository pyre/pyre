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
    # inspect {value}
    # first, check whether we were passed an evaluator
    if isinstance(value, Node.Evaluator):
        return Node(value=None, evaluator=value, **kwds)
    # perhaps {value} is another node
    if isinstance(value, Node):
        return value.newReference(**kwds)
    # otherwise, build a literal
    return Node(value=value, evaluator=None, **kwds)


# predicates
def isExpression(string):
    """
    Check whether {string} is an expression

    Currently, this predicate checks only for the presence of balanced pairs of braces; it
    doesn't perform any other syntax or validity tests
    """
    # get the Expression evaluator class
    from .Expression import Expression
    # ask its scanner whether {string} is a match
    return Expression._scanner.match(string)


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


def literal(value):
    """
    Create an evaluator that always returns the given value
    """
    from .Literal import Literal
    return Literal(value)


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


# debugging support
_metaclass_Node = type
_metaclass_Evaluator = type


def debug():
    """
    Attach ExtentAware as the metaclass of Node and Evaluator so we can verify that all
    instances of these classes are properly garbage collected
    """
    from ..patterns.ExtentAware import ExtentAware
    global _metaclass_Node, _metaclass_Evaluator
    _metaclass_Node = ExtentAware
    _metaclass_Evaluator = ExtentAware

    return
    

# end of file 
