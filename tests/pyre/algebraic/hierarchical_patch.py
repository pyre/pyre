#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Verify that node updates propagate properly
"""


def test():
    import pyre.algebraic

    # create a model
    model = pyre.algebraic.hierarchicalModel()

    # register the nodes
    model["user.name"] = "Michael Aïvázis"
    model["user.email"] = "aivazis@caltech.edu"
    model["user.signature"] = model.expression("{user.name}+' -- '+{user.email}")

    # check the signature
    assert model["user.signature"] == "Michael Aïvázis -- aivazis@caltech.edu"

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
