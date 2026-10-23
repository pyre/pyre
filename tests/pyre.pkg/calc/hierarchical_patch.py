#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that node updates propagate properly
"""


def test():
    """
    Build an expression over two nodes, change one of them, and check that the expression
    follows
    """
    # access the package
    import pyre.calc

    # create a model
    model = pyre.calc.model()

    # register the nodes
    model["user.name"] = "Michael Aïvázis"
    # under a common level of the hierarchy
    model["user.email"] = "michael.aivazis@orthologue.com"
    # along with an expression that refers to its siblings by their full names
    model["user.signature"] = model.expression("{user.name}+' -- '+{user.email}")

    # check the signature
    assert model["user.signature"] == "Michael Aïvázis -- michael.aivazis@orthologue.com"

    # give one of the nodes a new value
    model["user.email"] = "michael.aivazis@para-sim.com"

    # the signature follows
    assert model["user.signature"] == "Michael Aïvázis -- michael.aivazis@para-sim.com"

    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
