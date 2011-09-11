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
    import pyre.calc

    # build a model
    model = pyre.calc.model(name="expression_escaped")

    # escaped macro delimiters
    try:
        pyre.calc.expression(formula=r"{{production}}", model=model)
        assert False
    except pyre.calc.EmptyExpressionError:
        pass

    # and another
    try:
        pyre.calc.expression(formula=r"{{{{cost per unit}}}}", model=model)
        assert False
    except pyre.calc.EmptyExpressionError:
        pass

    # finally
    tricky = pyre.calc.expression(formula=r"{{{number of items}}}", model=model)
    # check that the escaped delimiters were processed correctly
    try:
        tricky.value
        assert False
    except tricky.UnresolvedNodeError:
        pass

    return


# main
if __name__ == "__main__":
    # request debugging support for the pyre.calc package
    pyre_debug = { "pyre.calc" }
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()
    # verify reference counts
    # for nodes
    from pyre.calc.Node import Node
    # print(tuple(Node._pyre_extent))
    assert tuple(Node._pyre_extent) == ()


# end of file 
