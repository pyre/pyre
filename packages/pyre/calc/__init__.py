# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
This package provides the implementation of a simple evaluation network.

There are three fundamental abstractions: variables, operators, and literals. Variables hold
the values computed by the evaluation network, operators compute their values by acting on the
values of other nodes, and literals encapsulate foreign objects, such as numeric constants.
These abstractions provide the machinery for representing arbitrary expressions as graphs.

The interesting aspect of this package is that nodal values get updated automatically when the
values of any of the nodes in their domain change. Nodes keep track of the set of dependents
that are interested in their values and post notifications when their values change.

In addition, this package provides {Model}, a simple manager for evaluation nodes. Beyond node
storage, {Model} enables the naming of nodes and can act as the name resolution context for
{Expression} nodes, which evaluate strings with arbitrary python expressions that may involve
the values of other nodes in the model. The other nodes provided here operate independently of
{Model}. However, it is a good idea to build some kind of container to hold nodes while the
evaluation graph is in use.

Simple examples of the use of the ideas in this package are provided in the unit tests. For a
somewhat more advanced example, take a look at {pyre.config.Configurator}, which is a {Model}
that builds an evaluation network out of the traits of pyre components, so that trait settings
can refer to the values of other traits in the configuration files.
"""


# implementation note: these factories are functions (rather than a raw import of the
# corresponding constructor) in order to prevent the secondary {import} from happening when the
# package itself is first imported. this enables the package to override compile time settings
# and makes it possible to implement the {debug} capability


# factories
# model
def model(*, name, **kwds):
    """
    Build a node container that specializes in names that have encoded hierarchical levels,
    such as file paths or namespaces
    """
    from .HierarchicalModel import HierarchicalModel
    return HierarchicalModel(name=name, **kwds)


# nodes
def var(value=None):
    """
    Build a variable, i.e. a node that can hold an arbitrary value
    """
    # get the base node
    from .Node import Node
    # build a variable and return it
    return Node.variable(value=value)


def expression(*, formula, model):
    """
    Build a new node that evaluates a {formula} that involves the names of other nodes as
    resolved in the symbol table {model}.
    """
    # build the node and return it
    return model.parse(expression=formula)


def average(*operands):
    """
    Compute the average of a collection of nodes
    """
    # access the constructor
    from .Node import average
    # build the node and return it
    return average(operands=operands)


def count(*operands):
    """
    Compute the length of a collection of nodes
    """
    # access the constructor
    from .Node import count
    # build the node and return it
    return count(operands=operands)


def max(*operands):
    """
    Compute the minimum of a collection of nodes
    """
    # access the constructor
    from .Node import max
    # build the node and return it
    return max(operands=operands)


def min(*operands):
    """
    Compute the minimum of a collection of nodes
    """
    # access the constructor
    from .Node import min
    # build the node and return it
    return min(operands=operands)


def product(*operands):
    """
    Compute the sum of a collection of nodes
    """
    # access the constructor
    from .Node import product
    # build the node and return it
    return product(operands=operands)


def sum(*operands):
    """
    Compute the sum of a collection of nodes
    """
    # access the constructor
    from .Node import sum
    # build the node and return it
    return sum(operands=list(operands))


# exceptions
from .exceptions import EmptyExpressionError


# debugging support
_metaclass_Node = type

def debug():
    """
    Attach {ExtentAware} as the metaclass of {Node} so we can verify that all instances of
    this class are properly garbage collected
    """
    from ..patterns.ExtentAware import ExtentAware
    global _metaclass_Node
    _metaclass_Node = ExtentAware

    return
    

# end of file 
