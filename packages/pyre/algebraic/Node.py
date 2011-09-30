# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
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
from .Unresolved import Unresolved


# declaration of the base node
class Node(AbstractNode, Number, Ordering, Boolean):
    """
    The base class for hierarchies that implement the algebraic protocol

    The example nodes in this package use the full set of protocols provided.
    """


    # types: hooks for implementing the expression graph construction
    # structural
    leaf = Leaf
    composite = Composite
    # functional
    literal = Literal
    variable = None
    operator = None
    expression = None
    unresolved = Unresolved


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

class expression(Node, Expression, Node.composite):
    """
    Concrete class for encapsulating macros
    """

# patch to base class
Node.variable = variable
Node.operator = operator
Node.expression = expression


# end of file 
