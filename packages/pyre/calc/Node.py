# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# externals
import pyre.algebraic
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
class Node(pyre.algebraic.AbstractNode, pyre.algebraic.Arithmetic, metaclass=_metaclass_Node):
    """
    The base class for lazily evaluated nodes. It employs the memoized evaluation strategy so
    that nodes have their values recomputed on demand.
    """


    # types: hooks for implementing the expression graph construction
    # the mix-ins
    leaf = pyre.algebraic.Leaf
    literal = pyre.algebraic.Literal
    composite = pyre.algebraic.Composite
    const = pyre.algebraic.Const
    memo = pyre.algebraic.Memo
    observer = pyre.algebraic.Observer
    observable = pyre.algebraic.Observable
    # the functional; they will be patched below with my subclasses
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
class variable(Node.observable, pyre.algebraic.Variable, Node.leaf, Node):
    """
    Concrete class for encapsulating the user accessible nodes
    """

# operators
class operator(Node.memo, Node.observer, pyre.algebraic.Operator, Node.composite, Node):
    """
    Concrete class for encapsulating operations among nodes
    """

# expressions
class expression(Node.memo, Node.observer, pyre.algebraic.Expression, Node.composite, Node):
    """
    Concrete class for encapsulating macros
    """

# interpolations
class interpolation(Node.memo, Node.observer, pyre.algebraic.Interpolation, Node.composite, Node):
    """
    Concrete class for encapsulating simple string interpolation
    """

# references
class reference(Node.observer, pyre.algebraic.Reference, Node.composite, Node):
    """
    Concrete class for encapsulating references to other nodes
    """

# unresolved nodes
class unresolved(Node.observable, pyre.algebraic.Unresolved, Node.leaf, Node):
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
Node.reference = reference
Node.unresolved = unresolved


# end of file 
