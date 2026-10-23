#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that syntax errors in expressions are caught
"""


def test():
    # access the package
    import pyre.calc

    # build a model
    model = pyre.calc.model()

    # check that an unbalanced open brace is caught
    try:
        # build an expression with an open brace that is never closed
        model.expression(value="{production")
        # which should have failed
        assert False
    # if it fails as expected
    except model.ExpressionSyntaxError:
        # all is good
        pass

    # check that an unbalanced close brace is caught
    try:
        # build an expression with a close brace that was never opened
        model.expression(value="production}")
        # which should have failed
        assert False
    # if it fails as expected
    except model.ExpressionSyntaxError:
        # all is good
        pass

    # check that an unbalanced parenthesis is caught
    try:
        # build an expression with a parenthesis that is never closed
        model.expression(value="{production}({shipping}")
        # which should have failed
        assert False
    # if it fails as expected
    except model.ExpressionSyntaxError:
        # all is good
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
