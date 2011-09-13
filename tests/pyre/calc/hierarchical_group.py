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
    model["pyre.user.name"] = "Michael Aïvázis"
    model["pyre.user.email"] = "aivazis@caltech.edu"
    model["pyre.user.affiliation"] = "California Institute of Technology"
    model["pyre.user.signature"] = "{user.name}+' -- '+{user.email}"
    model["pyre.user.telephone"] = "+1 626.395.3424"

    # and some aliases
    model.alias(alias="χρήστης", canonical="pyre.user")
    model.alias(alias="χρήστης.όνομα", canonical="pyre.user.name")

    # here are the canonical names
    names = { "name", "email", "affiliation", "signature", "telephone" }

    # get all the subnodes of "user"
    assert len(names) == len(tuple(model.children(root="pyre.user")))
    for key, identifier, name, fqname, node in model.children(root="user"):
        # check that we got the canonical name
        assert name in names
        # and the correct node
        assert model._resolve(name=fqname) == (node, identifier)

    # repeat with the alias "χρήστης"
    assert len(names) == len(tuple(model.children(root="χρήστης")))
    for key, identifier, name, fqname, node in model.children(root="χρήστης"):
        # check that we got the canonical name
        assert name in names
        # and the correct node
        assert model._resolve(name=fqname) == (node, identifier)

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file 
