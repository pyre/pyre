# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


# so I can hold on to my model without making cycles
import weakref


# class declaration
class Expression:
    """
    Support for building evaluation graphs involving nodes that have names registered with an
    {AbstractModel} instance
    """


    # exceptions
    from .exceptions import (
        CircularReferenceError,
        EmptyExpressionError, ExpressionSyntaxError, UnresolvedNodeError,
        EvaluationError )


    # public data
    formula = None # the expression supplied by the client
    operands = () # the list of nodes i refer to


    @property
    def value(self):
        """
        Compute and return my value
        """
        # attempt
        try:
            # to evaluate my program
            return eval(self._program, {'model' : self._model })
        # if i run into unresolved nodes
        except self.UnresolvedNodeError:
            # report it
            raise
        # other errors
        except Exception as error: 
            # are reported as evaluation errors
            raise self.EvaluationError(node=self, error=error) from error
                
        # UNREACHABLE
        return


    # meta methods
    def __init__(self, model, expression, program, operands, **kwds):
        super().__init__(**kwds)
        self.formula = expression
        self._program = program
        self._model = weakref.proxy(model)
        self.operands = operands
        return


    # private data
    _model = None # my symbol table
    _program = None # the compiled form of my expression


# end of file 
