# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to the node algebra
from .Number import Number
from .Ordering import Ordering
from .Boolean import Boolean

# declaration
class Node(Number, Ordering, Boolean):
    """
    This is the base class for hierarchies that implement the algebraic protocol

    The base classes {Number}, {Ordering} and {Boolean} overload the methods that are invoked
    by the evaluation of expressions involving python operators. The implementation of these
    methods expect {Node} to provide access to two subclasses, {Literal} and {Operator}, that
    are used to build a representation of the python expression. {Literal} is used to
    encapsulate objects that are foreign to the {Node} class hierarchy, e.g. integers, and
    {Operation} encodes the operator encountered and its operands. This access must be provided
    through two {Node} properties, {literal} and {operation}, which provide an extra layer of
    abstraction by hiding the actual {Node} subclasses.
    """


    # traversal of the nodes in my expression graph
    @property
    def dependencies(self):
        """
        Traverse my expression graph looking for nodes i depend on
        """
        # just return myself
        yield self
        # and no more
        return


    # interface
    def eval(self, **kwds):
        """
        Compute the value of my expression graph
        """
        raise NotImplementedError(
            "class {.__class__.__name__!r} must implement 'eval'".format(self))


    def dfs(self, **kwds):
        """
        Traverse an expression graph in depth-first order
        """
        # by default, node instances yield themselves
        yield self
        # and no more
        return


    def patch(self, *args, **kwds):
        """
        Sentinel method for node patching in expression graphs
        """
        return


    # hooks for implementing the expression graph construction
    # the default implementation provided by this package uses the classes defined here
    @property
    def literal(self):
        """
        Grant access to the subclass used to encapsulate foreign values
        """
        # important: must return a type, not an instance
        from .Literal import Literal
        return Literal


    @property
    def operation(self):
        """
        Grant access to the subclass used to encapsulate one of the supported operations
        """
        # important: must return a type, not an instance
        from .Operator import Operator
        return Operator


# end of file 
