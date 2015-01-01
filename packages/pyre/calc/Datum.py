# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


# superclass
from ..algebraic.AbstractNode import AbstractNode


# declaration of the base node
class Datum(AbstractNode):
    """
    The base class for nodes that have values
    """


    # types
    mapping = None
    sequence = None
    expression = None
    interpolation = None
    reference = None
    unresolved = None

    # exceptions; included here for client convenience
    from .exceptions import (
        EmptyExpressionError, ExpressionSyntaxError, EvaluationError,
        UnresolvedNodeError
        )


    # public data
    @property
    def value(self):
        """
        Get my value
        """
        # delegate
        return self.getValue()


    @value.setter
    def value(self, value):
        """
        Set my value
        """
        # delegate
        return self.setValue(value=value)


    # interface
    def ref(self, **kwds):
        """
        Build and return a reference to me
        """
        # use the class factory to make one and return it
        return self.reference(operands=[self], **kwds)


# end of file
