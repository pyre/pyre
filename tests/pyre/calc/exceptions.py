#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Tests for all the exceptions raised by this package
"""


def test():

    import pyre.calc
    from pyre.calc.exceptions import (
        NodeError, CircularReferenceError, EvaluationError,
        ExpressionError, EmptyExpressionError, ExpressionSyntaxError, UnresolvedNodeError )

    try:
        raise NodeError(description="generic error")
    except NodeError as error:
        pass

    try:
        raise CircularReferenceError(node=None, path=None)
    except CircularReferenceError as error:
        pass

    try:
        raise EvaluationError(node=None, error=None)
    except EvaluationError as error:
        pass

    try:
        raise EmptyExpressionError(formula=None)
    except EmptyExpressionError as error:
        pass

    try:
        raise ExpressionSyntaxError(formula=None, error=None)
    except ExpressionError as error:
        pass

    try:
        raise UnresolvedNodeError(node=None, name=None)
    except UnresolvedNodeError as error:
        pass

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file 
