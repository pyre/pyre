#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that syntax errors in expressions are caught
"""


def test():
    import pyre.algebraic

    # build a model
    model = pyre.algebraic.model()

    # unbalanced open brace
    try:
        pyre.algebraic.expression(value="{production", model=model)
        assert False
    except model.ExpressionSyntaxError:
        pass

    # unbalanced open brace
    try:
        pyre.algebraic.expression(value="production}", model=model)
        assert False
    except model.ExpressionSyntaxError:
        pass

    # unbalanced parenthesis
    try:
        pyre.algebraic.expression(value="{production}({shipping}", model=model)
        assert False
    except model.ExpressionSyntaxError:
        pass

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file 
