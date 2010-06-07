#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Verify that syntax errors in expressions are caught
"""


import pyre.calc


def test():
    # build a model
    model = pyre.calc.newModel(name="expression_escaped")

    # escaped macro delimiters
    literal = pyre.calc.newNode(
        value=pyre.calc.expression(formula=r"{{production}}", model=model))
    # check that the escaped delimiters were processed correctly
    assert literal.value == r"{{production}}"

    return


# main
if __name__ == "__main__":
    # get the extent manager
    from pyre.patterns.ExtentAware import ExtentAware
    # install it
    pyre.calc._metaclass_Node = pyre.calc._metaclass_Evaluator = ExtentAware
    # run the test
    test()
    # verify reference counts
    # for nodes
    from pyre.calc.Node import Node
    # print(tuple(Node._pyre_extent))
    assert tuple(Node._pyre_extent) == ()
    # print(tuple(Node.Evaluator._pyre_extent))
    assert tuple(Node.Evaluator._pyre_extent) == ()


# end of file 
