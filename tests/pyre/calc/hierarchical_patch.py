#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Sanity check: verify that the package is accessible
"""


def test():
    import pyre.calc

    # create a model
    model = pyre.calc.hierarchicalModel(name="sample")

    # register the nodes
    model["user.name"] = "Michael Aïvázis"
    model["user.email"] = "aivazis@caltech.edu"
    model["user.signature"] = "{user.name}+' -- '+{user.email}"

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
