#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


"""
Sanity check: verify that the package is accessible
"""


def test():
    import pyre.calc

    # create a model
    model = pyre.calc.newHierarchicalModel(name="sample")

    # register the nodes
    model["user.name"] = "Michael Aïvázis"
    model["user.email"] = "aivazis@caltech.edu"
    model["user.affiliation"] = "California Institute of Technology"
    model["user.signature"] = "{user.name}+' -- '+{user.email}"
    model["user.telephone"] = "+1 626.395.3424"

    # and some aliases
    model.alias(alias="χρήστης", canonical="user")
    model.alias(alias="χρήστης.όνομα", canonical="user.name")

    # here are the canonical names
    names = { "name", "email", "affiliation", "signature", "telephone" }

    # get all the subnodes of "user"
    assert len(names) == len(tuple(model.children(root="user")))
    for key, name, fqname, node in model.children(root="user"):
        # check that we got the canonical name
        assert name in names
        # and the correct node
        assert model.resolve(name=fqname) == node
    # repeat with the alias "χρήστης"
    assert len(names) == len(tuple(model.children(root="χρήστης")))
    for key, name, fqname, node in model.children(root="χρήστης"):
        # check that we got the canonical name
        assert name in names
        # and the correct node
        assert model.resolve(name=fqname) == node

    return


# main
if __name__ == "__main__":
    test()


# end of file 
