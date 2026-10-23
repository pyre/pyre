#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that an interpolation with an operand that is {None} is {None}, rather than text that
spells it
"""


def test() -> None:
    """
    Splice a node that holds {None} into an interpolation, alone and with some text, then give
    the node a value
    """
    # access the package
    import pyre.calc

    # set up the model
    model = pyre.calc.model()
    # a node that holds {None}
    model["home"] = None
    # an interpolation that splices it into some text
    model["bin"] = model.interpolation("{home}/bin")
    # and one that refers to it alone
    model["alias"] = model.interpolation("{home}")

    # neither has any text to offer
    assert model["bin"] is None
    # and neither stands in for it
    assert model["alias"] is None

    # give the node a value
    model["home"] = "/opt/local"
    # the interpolation with text follows it
    assert model["bin"] == "/opt/local/bin"
    # and so does the one without
    assert model["alias"] == "/opt/local"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
