#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Sanity check: instantiate a hierarchical model
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

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file 
