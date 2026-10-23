#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Tests for all the exceptions raised by this package
"""


def test():
    # the exceptions of the package
    from pyre.calc.exceptions import (
        EvaluationError,
        ExpressionError,
        EmptyExpressionError,
        ExpressionSyntaxError,
        UnresolvedNodeError,
    )

    # attempt to
    try:
        # raise an evaluation error
        raise EvaluationError(node=None, error=None)
    # and catch it
    except EvaluationError:
        # as expected
        pass

    # attempt to
    try:
        # raise an empty expression error
        raise EmptyExpressionError(formula=None)
    # and catch it
    except EmptyExpressionError:
        # as expected
        pass

    # attempt to
    try:
        # raise a syntax error in an expression
        raise ExpressionSyntaxError(formula=None, error=None)
    # and catch it as an expression error, its base class
    except ExpressionError:
        # as expected
        pass

    # attempt to
    try:
        # raise an unresolved node error
        raise UnresolvedNodeError(node=None, name=None)
    # and catch it
    except UnresolvedNodeError:
        # as expected
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # do...
    test()


# end of file
