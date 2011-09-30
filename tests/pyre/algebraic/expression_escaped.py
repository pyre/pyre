#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that syntax errors in expressions are caught
"""


def test():
    import pyre.algebraic

    # build a model
    model = pyre.algebraic.model(name="expression_escaped")

    # escaped macro delimiters
    try:
        pyre.algebraic.expression(formula=r"{{production}}", model=model)
        assert False
    except model.EmptyExpressionError:
        pass

    # and another
    try:
        pyre.algebraic.expression(formula=r"{{{{cost per unit}}}}", model=model)
        assert False
    except model.EmptyExpressionError:
        pass

    # finally
    tricky = pyre.algebraic.expression(formula=r"{{{number of items}}}", model=model)
    # check that the escaped delimiters were processed correctly
    try:
        tricky.value
        assert False
    except tricky.UnresolvedNodeError:
        pass

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file 
