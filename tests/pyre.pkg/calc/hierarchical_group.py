#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify we can extract all names under a given level in the hierarchy
"""


def test():
    # access the package
    import pyre.calc

    # create a model
    model = pyre.calc.model()

    # register the user name
    model["pyre.user.name"] = "Michael Aïvázis"
    # the email
    model["pyre.user.email"] = "michael.aivazis@orthologue.com"
    # the affiliation
    model["pyre.user.affiliation"] = "orthologue"
    # the signature
    model["pyre.user.signature"] = "{pyre.user.name}+' -- '+{pyre.user.email}"
    # and the telephone
    model["pyre.user.telephone"] = "+1 626.395.3424"

    # alias the user level
    model.alias(alias="χρήστης", target="pyre.user")
    # and the name, relative to the alias
    model.alias(base="χρήστης", alias="όνομα", target="pyre.user.name")

    # here are the canonical names
    names = {
        "pyre.user." + tag for tag in ("name", "email", "affiliation", "signature", "telephone")
    }

    # get all the subnodes of "user"
    target = "pyre.user"
    # check that we get all of them
    assert len(names) == len(tuple(model.children(key=target)))
    # go through them
    for key, node in model.children(key=target):
        # check that we got the correct node
        assert model._nodes[key] is node

    # repeat with the alias "χρήστης"
    target = "χρήστης"
    # check that we get all of them
    assert len(names) == len(tuple(model.children(key=target)))
    # go through them
    for key, node in model.children(key=target):
        # check that we got the correct node
        assert model._nodes[key] is node

    # visual check
    # model.dump()
    # all done
    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file
