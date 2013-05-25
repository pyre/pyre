# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# externals
from .. import algebraic
# local operators
from .Average import Average
from .Count import Count
from .Maximum import Maximum
from .Minimum import Minimum
from .Product import Product
from .Sum import Sum

# my metaclass: defined in the package initialization file
from . import _metaclass_Node


# declaration of the base node
class Node(algebraic.AbstractNode, algebraic.Arithmetic, metaclass=_metaclass_Node):
    """
    The base class for lazily evaluated nodes. It employs the memoized evaluation strategy so
    that nodes have their values recomputed on demand.
    """


    # types: hooks for implementing the expression graph construction
    # the mix-ins
    leaf = algebraic.Leaf
    literal = algebraic.Literal
    composite = algebraic.Composite
    const = algebraic.Const
    # evaluation strategies
    memo = algebraic.Memo
    converter = algebraic.Converter
    observer = algebraic.Observer
    observable = algebraic.Observable
    # the functionals; they will be patched below with my subclasses
    variable = None
    operator = None
    expression = None
    interpolation = None
    reference = None
    unresolved = None


# literals
class literal(Node.const, Node.literal, Node):
    """
    Concrete class for representing foreign values
    """

# variables
class variable(Node.memo, Node.converter, Node.observable, algebraic.Variable, Node.leaf, Node):
    """
    Concrete class for encapsulating the user accessible nodes
    """

# operators
class operator(Node.memo, Node.converter, Node.observer, algebraic.Operator, Node.composite, Node):
    """
    Concrete class for encapsulating operations among nodes
    """

# expressions
class expression(Node.memo, Node.converter, 
                 Node.observer, algebraic.Expression, Node.composite, Node):
    """
    Concrete class for encapsulating macros
    """

# interpolations
class interpolation(Node.memo, Node.converter, 
                    Node.observer, algebraic.Interpolation, Node.composite, Node):
    """
    Concrete class for encapsulating simple string interpolation
    """

# references
class reference(Node.memo, Node.converter,
                Node.observer, algebraic.Reference, Node.composite, Node):
    """
    Concrete class for encapsulating references to other nodes
    """

# unresolved nodes
class unresolved(Node.observable, algebraic.Unresolved, Node.leaf, Node):
    """
    Concrete class for representing unknown nodes
    """

# local operators
class average(Node.memo, Node.observer, Average, Node.composite, Node):
    """
    Concrete class for representing the average value of a set of nodes
    """

class count(Node.memo, Node.observer, Count, Node.composite, Node):
    """
    Concrete class for representing the count of a set of nodes
    """

class max(Node.memo, Node.observer, Maximum, Node.composite, Node):
    """
    Concrete class for representing the maximum value of a set of nodes
    """

class min(Node.memo, Node.observer, Minimum, Node.composite, Node):
    """
    Concrete class for representing the minimum value of a set of nodes
    """

class product(Node.memo, Node.observer, Product, Node.composite, Node):
    """
    Concrete class for representing the product of nodes
    """

class sum(Node.memo, Node.observer, Sum, Node.composite, Node):
    """
    Concrete class for representing the sum of nodes
    """


# patch the base class
Node.literal = literal
Node.variable = variable
Node.operator = operator
Node.expression = expression
Node.interpolation = interpolation
Node.reference = reference
Node.unresolved = unresolved


# end of file 
