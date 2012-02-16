# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
This package provides the machinery for implementing deferred evaluation in python.

The strategy is to capture arithmetic operations among a collection of instances and build an
expression graph using instances of the classes in this package as nodes. Requesting the value
of some node in the graph triggers the actual evaluation.

There are multiple layers of building blocks provided in this package. The fundamental layer is
formed by the three classes {Number}, {Ordering} and {Boolean}. The provide overloaded version
of the various python operators that can be used to form expressions. Their implementations do
not carry out any evaluations; instead, they access the interface provided by their operands to
construct the expression graph.

The base layer is formed by the base class of the expression graph nodes. This class is
responsible for assembling all the parts necessary to build functioning expression graphs. The
main challenge is that the node class provided in this package is unlikely to be sufficient for
your purposes, yet all the higher layer classes must derive from it. This is an instance of a
general problem with class hierarchies, where some behavior is defined by the base class that
must be overridden without having to reimplement all the classes that derive from it. This
package solves this problem requiring your base node class to provide access to all its
subclasses that participate in the expression graph. Minor trickery is involved, and the idea
should be fairly clear.

The structural layer is formed by the mix-in classes {Leaf} and {Composite} that provide
the interface for traversing the expression graph. Each concrete node must derive from one of
these. If your particular needs require fancier behavior than what is provided, feel free to
subclass them and use them as bases for your concrete nodes.

The functional layer is formed by the mix-in classes {Literal}, {Variable} and {Operator}.
Variables are the nodes that you expose to your users to create and operate on; operators are
the encapsulation of the various operations defined on your variables; and literals are the
constants that show up in your expressions, such as integers, that are not conceptually part of
the space of variables.

You are responsible for putting all this together by providing a class that derives from {Node}
and provides an implementation of the required {AbstractNode} interface. Take a look at {Node}
for an example of how the simple concrete nodes in this package are assembled
"""


# access to the building blocks in this package
from .AbstractNode import AbstractNode
from .Memo import Memo
from .Cast import Cast
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
from .Reference import Reference
from .Unresolved import Unresolved


# the base class of the simple concrete nodes in this package
from .Node import Node
# grant users access to the factory of the sample concrete nodes
var = Node.variable


# expression nodes
def expression(*, formula, model):
    """
    Build a new node that evaluates a {formula} that involves nodes in the {model}
    """
    return model.expression(formula)


def interpolation(*, text, model):
    """
    Build a new node that builds a string out of the values of other nodes in the {model}
    """
    return model.interpolation(text)


# access to the model factory
from .SymbolTable import SymbolTable as model
from .Hierarchical import Hierarchical as hierarchicalModel


# clean up
del Node


# end of file 
