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


# variables
class variable(Node, Node.leaf, Variable):
    """
    Concrete class for encapsulating the user accessible nodes
    """

# operators
class operator(Node, Node.composite, Operator):
    """
    Concrete class for encapsulating operations among nodes
    """

# patch to base class
Node.variable = variable
Node.operator = operator


# end of file 
