#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that node resolution works
"""


def test():
    # access the package
    import pyre.calc

    # set up the model
    model = pyre.calc.model()

    # set up an expression with an unresolved node
    model["price"] = model.expression(value="2*{production}")

    # ask for the price
    try:
        # which should fail since the production is unknown
        model["price"]
        # so we should never get here
        assert False
    # if it fails as expected
    except model.UnresolvedNodeError as error:
        # get the placeholder the model made for the production
        unresolved = model.retrieve(name="production")
        # check that the error carries it
        assert error.node is unresolved
        # and its name
        assert error.name == "production"

    # resolve the node
    p = 80.0
    # by giving the production a value
    model["production"] = p

    # ask for the price again
    assert model["production"] == p
    # the price is resolved and sees the production
    assert model["price"] == 2 * p

    # make a change
    p = 100.0
    # to the production
    model["production"] = p
    # check again
    assert model["production"] == p
    # the price follows the production
    assert model["price"] == 2 * p

    # force a node substitution
    m = 60
    # register the materials
    model["materials"] = m
    # replace the production with an expression that depends on the materials
    model["production"] = model.expression(value="2*{materials}")
    # check again
    assert model["materials"] == m
    # the production is computed from the materials
    assert model["production"] == 2 * m
    # and the price follows the substituted production
    assert model["price"] == 4 * m

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
