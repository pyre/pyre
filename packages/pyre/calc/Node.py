# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# access to my metaclass, as specified in the module initialization file; for debugging
from . import _metaclass_Node
# expression support
from ..algebraic.Node import Node as Base
# dependent notifications
from ..patterns.Observable import Observable


class Node(Base, Observable, metaclass=_metaclass_Node):
    """
    This is the base class for the nodes that appear in lazily evaluated expression graphs. See
    {pyre.algebraic.Node} for a discussion.

    Its main purpose is to override the {variable} and {operator} factories in its base class
    to provide access to the locally declared classes.
    """

    # types
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


    @property
    def literal(self):
        """
        Grant access to the subclass used to encapsulate literals
        """
        # important: must return a type, not an instance
        from .Literal import Literal
        return Literal


    # interface
    def reference(self):
        """
        Build and return a reference to me
        """
        # access the constructor
        from .Reference import Reference
        # make one
        return Reference(node=self)


# end of file 
