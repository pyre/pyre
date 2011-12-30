#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that circular dependencies are caught properly
"""


def test():
    import pyre.algebraic

    # a model
    model = pyre.algebraic.model(name="circular")

    # self reference

    try:
        model["cost"] = "{cost}"
        assert False
    except model.CircularReferenceError:
        pass

    # another model
    model = pyre.algebraic.model(name="circular")
    # now validate the graph, expecting the circular reference to raise an exception
    try:
        # a cycle
        model["cost"] = "{price}"
        model["price"] = "{cost}"
        assert False
    except model.CircularReferenceError:
        pass

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file 
