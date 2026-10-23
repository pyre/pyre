#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that model initialization fails correctly in the presence of expressions that cannot be
evaluated even though they have no syntax errors
"""


def test():
    # access the package
    import pyre.calc

    # a model
    model = pyre.calc.model()
    # the production cost
    model["production"] = 80.0
    # the shipping cost
    model["shipping"] = 20.0
    # an expression that is syntactically correct but applies {&} to floats
    model["cost"] = model.expression("{production}&{shipping}")

    # attempt to
    try:
        # evaluate the bad expression
        model["cost"]
        # which should have failed
        assert False
    # if it fails as expected
    except model.EvaluationError:
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
