#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that expressions work
"""


def test():
    # access the package
    import pyre.calc

    # set up the model
    model = pyre.calc.model()

    # the production cost
    p = 80.0
    # and the shipping cost
    s = 0.25 * 80
    # register the production cost
    model["production"] = p
    # and the shipping cost
    model["shipping"] = s
    # the total cost is their sum
    model["cost"] = model.expression("{production}+{shipping}")
    # and the price doubles it
    model["price"] = model.expression("2*{cost}")

    # check the values
    # check the production cost
    assert model["production"] == p
    # the shipping cost
    assert model["shipping"] == s
    # the total cost
    assert model["cost"] == p + s
    # and the price
    assert model["price"] == 2 * (p + s)

    # expressions refer to their operands indirectly, so they see the new values of their
    # operands

    # make a change to the production cost
    p = 100.0
    # and hand it to the model
    model["production"] = p

    # check again
    # check the production cost
    assert model["production"] == p
    # the shipping cost is unaffected
    assert model["shipping"] == s
    # the total cost sees the change
    assert model["cost"] == p + s
    # and so does the price
    assert model["price"] == 2 * (p + s)

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
