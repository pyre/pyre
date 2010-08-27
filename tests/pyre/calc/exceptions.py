#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Tests for all the exceptions raised by this package
"""


def test():

    import pyre.calc
    from pyre.calc.exceptions import (
        NodeError, CircularReferenceError, DuplicateNodeError, EvaluationError,
        ExpressionError, UnresolvedNodeError )

    try:
        raise NodeError(description="generic error")
    except NodeError as error:
        pass

    try:
        raise CircularReferenceError(node=None, path=None)
    except CircularReferenceError as error:
        pass

    try:
        raise DuplicateNodeError(model=None, node=None, name=None)
    except DuplicateNodeError as error:
        pass

    try:
        raise EvaluationError(evaluator=None, error=None)
    except EvaluationError as error:
        pass

    expression = pyre.calc.newNode(value=pyre.calc.expression(formula="2*2", model=None))
    try:
        raise ExpressionError(evaluator=expression._evaluator, error=None)
    except ExpressionError as error:
        pass

    try:
        raise UnresolvedNodeError(node=None, name=None)
    except UnresolvedNodeError as error:
        pass

    return


# main
if __name__ == "__main__":
    test()


# end of file 
