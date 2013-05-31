# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


# metaclass
from . import calculator


# declaration of the base node
class Node(metaclass=calculator):
    """
    The base class for lazily evaluated nodes
    """


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
        return self.setValue(value)


    # interface
    def ref(self, **kwds):
        """
        Build and return a reference to me
        """
        # use the class factory to make one and return it
        return self.reference(operands=[self], **kwds)
    

# end of file 
