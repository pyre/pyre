# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to my metaclass, as specified in the module initialization file; for debugging
from . import _metaclass_Node
# expression support.  N.B.: inheriting from {pyre.algebraic.Node} does not currently work
# because {Observable} uses a weak key dictionary to store the registered callbacks and there
# is a conflict with {Ordering.__eq__} that causes an infinite recursion
from ..algebraic.Number import Number as Base
# dependent notifications
from ..patterns.Observable import Observable


# declaration
class Node(Base, Observable, metaclass=_metaclass_Node):
    """
    This is the base class for the nodes that appear in lazily evaluated expression graphs. See
    {pyre.algebraic.Node} for a discussion.

    Its main purpose is to override the {variable} and {operator} factories in its base class
    to provide access to the locally declared classes.
    """


    # types
    @property
    def literal(self):
        """
        Grant access to the subclass used to encapsulate literals
        """
        # important: must return a type, not an instance
        from .Literal import Literal
        return Literal


    @property
    def variable(self):
        """
        Grant access to the subclass used to encapsulate variables
        """
        # important: must return a type, not an instance
        from .Variable import Variable
        return Variable


    @property
    def operator(self):
        """
        Grant access to the subclass used to encapsulate operators
        """
        # important: must return a type, not an instance
        from .Operator import Operator
        return Operator


    # public data
    @property
    def value(self):
        """
        Compute and return my value
        """
        raise NotImplementedError(
            "class {.__class__.__name__!r} must implement 'value'".format(self))


    @property
    def variables(self):
        """
        Traverse my expression graph and yield all the variables in my graph

        Variables are reported as many times as they show up in my graph. Clients that are
        looking for the set unique dependencies have to prune the results themselves.
        """
        raise NotImplementedError(
            "class {.__class__.__name__!r} must implement 'variables'".format(self))


    @property
    def operators(self):
        """
        Traverse my expression graph and yield all operators in my graph

        Operators are reported as many times as they show up in my graph. Clients that are
        looking for unique dependencies have to prune the results themselves.
        """
        raise NotImplementedError(
            "class {.__class__.__name__!r} must implement 'operators'".format(self))


    # interface
    def reference(self):
        """
        Build and return a reference to me
        """
        # access the constructor
        from .Reference import Reference
        # make one
        return Reference(node=self)


    def substitute(self, current, replacement):
        """
        Traverse my expression graph and replace all occurrences of node {current} with
        {replacement}.

        This method makes it possible to introduce cycles in the expression graph
        inadvertently. It is the client's responsibility to make sure that the graph remains
        cycle-free.
        """
        raise NotImplementedError(
            "class {.__class__.__name__!r} must implement 'substitute'".format(self))


# end of file 
