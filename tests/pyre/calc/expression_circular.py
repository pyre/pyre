#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify that circular dependencies are caught properly
"""


def test():
    import pyre.calc

    # a model
    model = pyre.calc.newModel(name="circular")

    # self reference
    cost = pyre.calc.newNode(value=pyre.calc.expression(formula="{cost}", model=model))
    model.register(name="cost", node=cost)

    try:
        model.validate()
        assert False
    except model.CircularReferenceError:
        pass

    # another model
    model = pyre.calc.newModel(name="circular")
    # a cycle
    cost = pyre.calc.newNode(value=pyre.calc.expression(formula="{price}", model=model))
    price = pyre.calc.newNode(value=pyre.calc.expression(formula="{cost}", model=model))
    # try to register one of them
    model.register(name="cost", node=cost)
    model.register(name="price", node=price)
    # now validate the graph, expecting the circular reference to raise an exception
    try:
        model.validate()
        assert False
    except model.CircularReferenceError:
        pass

    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file 
