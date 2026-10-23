#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that circular dependencies are caught properly
"""


def test():
    # access the package
    import pyre.calc

    # a model
    model = pyre.calc.model()

    # self reference
    try:
        # make a node that refers to itself
        model["cost"] = model.expression("{cost}")
        # which should have been detected
        assert False
    # if the cycle is detected
    except model.CircularReferenceError:
        # all is good
        pass

    # another model
    model = pyre.calc.model()
    # now validate the graph, expecting the circular reference to raise an exception
    try:
        # make a node that refers to another
        model["cost"] = model.expression("{price}")
        # which refers back to it, closing a cycle
        model["price"] = model.expression("{cost}")
        # which should have been detected
        assert False
    # if the cycle is detected
    except model.CircularReferenceError:
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
