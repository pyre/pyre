# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


import weakref
from .Node import Node
from .Dependent import Dependent


class Expression(Dependent, Node):
    """
    Support for building evaluation graphs involving nodes that have names registered with an
    {AbstractModel} instance
    """


    # types
    # nodes
    from .UnresolvedNode import UnresolvedNode
    # exceptions
    from .exceptions import (
        CircularReferenceError,
        EmptyExpressionError, ExpressionSyntaxError, UnresolvedNodeError,
        EvaluationError )


    # public data
    formula = None # the expression supplied by the client


    @property
    def value(self):
        """
        Compute and return my value
        """
        # if my cached value is invalid
        if self._value is None:
            # evaluate my program
            try:
                self._value = self._model.eval(self._program)
            except self.UnresolvedNodeError:
                raise
            # others are reported as evaluation errors
            except Exception as error:
                raise self.EvaluationError(node=self, error=error) from error
                
        # and return it
        return self._value


    # meta methods
    def __init__(self, model, expression, program, **kwds):
        super().__init__(**kwds)
        self.formula = expression
        self._program = program
        self._model = weakref.proxy(model)
        return


    # private data
    _program = None # the compiled form of my expression


# end of file 
