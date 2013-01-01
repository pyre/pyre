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
# evaluation strategy
from .Memo import Memo
from .Observer import Observer
from .Observable import Observable


# the auto node
class AutoNode(AbstractNode, Arithmetic, Ordering, Boolean):

    # the mix-ins
    leaf = Leaf
    literal = Literal
    composite = Composite
    const = Const
    memo = Memo
    observer = Observer
    observable = Observable
    # the functional; they will be patched below with my subclasses
    variable = None
    operator = None
    expression = None
    interpolation = None
    reference = None
    unresolved = None


# literals
class literal(AutoNode.const, AutoNode.literal, AutoNode):
    """
    Concrete class for representing foreign values
    """

# variables
class variable(AutoNode.observable, Variable, AutoNode.leaf, AutoNode):
    """
    Concrete class for encapsulating the user accessible nodes
    """

# operators
class operator(AutoNode.memo, AutoNode.observer, Operator, AutoNode.composite, AutoNode):
    """
    Concrete class for encapsulating operations among nodes
    """

# expressions
class expression(AutoNode.memo, AutoNode.observer, Expression, AutoNode.composite, AutoNode):
    """
    Concrete class for encapsulating macros
    """

# interpolations
class interpolation(AutoNode.memo, AutoNode.observer, Interpolation, AutoNode.composite, AutoNode):
    """
    Concrete class for encapsulating simple string interpolation
    """

# references
class reference(AutoNode.memo, AutoNode.observer, Reference, AutoNode.composite, AutoNode):
    """
    Concrete class for encapsulating references to other nodes
    """

# unresolved nodes
class unresolved(AutoNode.observable, Unresolved, AutoNode.leaf, AutoNode):
    """
    Concrete class for representing unknown nodes
    """


# patch base class
AutoNode.literal = literal
AutoNode.variable = variable
AutoNode.operator = operator
AutoNode.expression = expression
AutoNode.interpolation = interpolation
AutoNode.reference = reference
AutoNode.unresolved = unresolved


# end of file 
