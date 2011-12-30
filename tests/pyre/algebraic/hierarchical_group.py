#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


"""
Sanity check: verify that the package is accessible
"""


def test():
    import pyre.algebraic

    # create a model
    model = pyre.algebraic.hierarchicalModel(name="sample")

    # register the nodes
    model["pyre.user.name"] = "Michael Aïvázis"
    model["pyre.user.email"] = "aivazis@caltech.edu"
    model["pyre.user.affiliation"] = "California Institute of Technology"
    model["pyre.user.signature"] = "{pyre.user.name}+' -- '+{pyre.user.email}"
    model["pyre.user.telephone"] = "+1 626.395.3424"

    # and some aliases
    model.alias(alias="χρήστης", canonical="pyre.user")
    model.alias(alias="χρήστης.όνομα", canonical="pyre.user.name")

    # here are the canonical names
    names = { 
        "pyre.user." + tag
        for tag in ("name", "email", "affiliation", "signature", "telephone") }

    # get all the subnodes of "user"
    target = ["pyre", "user"]
    assert len(names) == len(tuple(model.children(key=target)))
    for key, node in model.children(key=target):
        # check that we got the correct node
        assert model._nodes[key] is node

    # repeat with the alias "χρήστης"
    target = ["χρήστης"]
    assert len(names) == len(tuple(model.children(key=target)))
    for key, node in model.children(key=target):
        # check that we got the correct node
        assert model._nodes[key] is node

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file 
