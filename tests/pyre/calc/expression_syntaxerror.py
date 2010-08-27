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


def test():
    import pyre.calc

    # build a model
    model = pyre.calc.newModel(name="expression_syntaxerror")

    # unbalanced parenthesis
    try:
        pyre.calc.newNode(
            evaluator=pyre.calc.expression(formula="{production}({shipping}", model=model))
        assert False
    except model.ExpressionError:
        pass

    return


# main
if __name__ == "__main__":
    # request debugging support for the pyre.calc package
    pyre_debug = { "pyre.calc" }
    # run the test
    test()
    # destroy the framework parts to make sure there are no excess nodes around
    import pyre
    pyre.executive.configurator = None
    # verify reference counts
    # for nodes
    from pyre.calc.Node import Node
    # print(tuple(Node._pyre_extent))
    assert tuple(Node._pyre_extent) == ()
    # print(tuple(Node.Evaluator._pyre_extent))
    assert tuple(Node.Evaluator._pyre_extent) == ()


# end of file 
