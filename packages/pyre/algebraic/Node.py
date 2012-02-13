# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


# my base class
from .AbstractNode import AbstractNode
# access to the node algebra mix-ins
from .Number import Number
from .Ordering import Ordering
from .Boolean import Boolean
# access to the structural mix-ins
from .Leaf import Leaf
from .Composite import Composite
# access to the functional mix-ins
from .Literal import Literal
from .Variable import Variable
from .Operator import Operator
from .Expression import Expression
from .Interpolation import Interpolation
from .Reference import Reference
from .Unresolved import Unresolved


# declaration of the base node
class Node(AbstractNode, Number, Ordering, Boolean):
    """
    The base class for hierarchies that implement the algebraic protocol

    The example nodes in this package use the full set of protocols provided. The evaluation
    strategy is direct, i.e. nodes the entire span of a node gets reevaluated whenever its
    value is requested. In practical terms, this is only useful as an example of the
    infrastructure provided by this package. Client code should consider deriving from {Memo}
    as well, which maintains a value cache and recomputes expression graphs only when the cache
    becomes invalid.
    """


    # types: hooks for implementing the expression graph construction
    # structural
    leaf = Leaf
    composite = Composite
    # functional; they will be patched below with my subclasses
    literal = None
    variable = None
    operator = None
    expression = None
    interpolation = None
    reference = None
    unresolved = None


# literals
class literal(Node, Literal, Node.leaf):
    """
    Concrete class for representing foreign values
    """

# variables
class variable(Node, Variable, Node.leaf):
    """
    Concrete class for encapsulating the user accessible nodes
    """

# operators
class operator(Node, Operator, Node.composite):
    """
    Concrete class for encapsulating operations among nodes
    """

# expressions
class expression(Node, Expression, Node.composite):
    """
    Concrete class for encapsulating macros
    """

# interpolations
class interpolation(Node, Interpolation, Node.composite):
    """
    Concrete class for encapsulating simple string interpolation
    """

# references
class reference(Node, Reference, Node.composite):
    """
    Concrete class for encapsulating references to other nodes
    """

# unresolved nodes
class unresolved(Node, Unresolved, Node.leaf):
    """
    Concrete class for representing unknown nodes
    """


# patch to base class
Node.literal = literal
Node.variable = variable
Node.operator = operator
Node.expression = expression
Node.interpolation = interpolation
Node.reference = reference
Node.unresolved = unresolved


# end of file 
