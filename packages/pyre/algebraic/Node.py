# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# my base class
from .AbstractNode import AbstractNode
# access to the node algebra mix-ins
from .Arithmetic import Arithmetic
from .Ordering import Ordering
from .Boolean import Boolean
# access to the structural mix-ins
from .Leaf import Leaf
from .Composite import Composite
from .Literal import Literal
# access to the functional mix-ins
from .Const import Const
from .Variable import Variable
from .Operator import Operator
from .Expression import Expression
from .Interpolation import Interpolation
from .Reference import Reference
from .Unresolved import Unresolved


# declaration of the base node
class Node(AbstractNode, Arithmetic, Ordering, Boolean):
    """
    The base class for hierarchies that implement the algebraic protocol
    """


    # types: hooks for implementing the expression graph construction
    # structural
    leaf = Leaf
    literal = Literal
    composite = Composite
    # functional; they will be patched below with my subclasses
    const = Const
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
class variable(Variable, Node.leaf, Node):
    """
    Concrete class for encapsulating the user accessible nodes
    """

# operators
class operator(Operator, Node.composite, Node):
    """
    Concrete class for encapsulating operations among nodes
    """

# expressions
class expression(Expression, Node.composite, Node):
    """
    Concrete class for encapsulating macros
    """

# interpolations
class interpolation(Interpolation, Node.composite, Node):
    """
    Concrete class for encapsulating simple string interpolation
    """

# references
class reference(Reference, Node.composite, Node):
    """
    Concrete class for encapsulating references to other nodes
    """

# unresolved nodes
class unresolved(Unresolved, Node.leaf, Node):
    """
    Concrete class for representing unknown nodes
    """


# patch base class
Node.literal = literal
Node.variable = variable
Node.operator = operator
Node.expression = expression
Node.interpolation = interpolation
Node.reference = reference
Node.unresolved = unresolved


# end of file 
