#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2023 all rights reserved
#


"""
Verify that node updates propagate properly
"""


def test():
    import pyre.calc

    # create a model
    model = pyre.calc.model()

    # register the nodes
    model["user.name"] = "Michael Aïvázis"
    model["user.email"] = "michael.aivazis@orthologue.com"
    model["user.signature"] = model.expression("{user.name}+' -- '+{user.email}")

    # check the signature
    assert model["user.signature"] == "Michael Aïvázis -- michael.aivazis@orthologue.com"

    # modify one of the nodes
    model["user.email"] = "michael.aivazis@orthologue.com"

    # check the new signature
    assert model["user.signature"] == "Michael Aïvázis -- michael.aivazis@orthologue.com"

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
