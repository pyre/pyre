#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Exercise the aliasing feature of hierarchical models
"""


def test():
    import pyre.algebraic

    # create a model
    model = pyre.algebraic.hierarchicalModel(name="sample")

    # register the nodes
    model["user.name"] = "Michael Aïvázis"
    model["user.email"] = "aivazis@caltech.edu"
    model["user.signature"] = "{user.name}+' -- '+{user.email}"
    # check the signature
    assert model["user.signature"] == "Michael Aïvázis -- aivazis@caltech.edu"

    # case 1: canonical does not exist, alias does not exist
    model.alias(alias="author.affiliation", canonical="user.affiliation")
    model["user.affiliation"] = "California Institute of Technology"
    assert model["author.affiliation"] == model["user.affiliation"]

    # case 2: canonical exists, alias does not
    model.alias(alias="author.signature", canonical="user.signature")
    # check the signature
    assert model["author.signature"] == model["user.signature"]

    # case 3: canonical does not exist, alias does
    model["author.telephone"] = "+1 626.395.3424"
    model.alias(alias="author.telephone", canonical="user.telephone")
    assert model["author.telephone"] == model["user.telephone"]

    # case 4: both are preëxisting nodes
    model["author.name"] = "TBD"
    model.alias(alias="author.name", canonical="user.name")
    assert model["author.name"] == model["user.name"]

    # check the final state
    assert model["user.name"] == "Michael Aïvázis"
    assert model["user.email"] == "aivazis@caltech.edu"
    assert model["user.telephone"] == "+1 626.395.3424"
    assert model["user.affiliation"] == "California Institute of Technology"
    assert model["user.signature"] == "Michael Aïvázis -- aivazis@caltech.edu"

    # and again through the aliases
    assert model["author.name"] == "Michael Aïvázis"
    try:
        model["author.email"]
        assert False
    except model.UnresolvedNodeError as error:
        pass
    assert model["author.telephone"] == "+1 626.395.3424"
    assert model["author.affiliation"] == "California Institute of Technology"
    assert model["author.signature"] == "Michael Aïvázis -- aivazis@caltech.edu"

    return


# main
if __name__ == "__main__":
    # skip pyre initialization since we don't rely on the executive
    pyre_noboot = True
    # run the test
    test()


# end of file 
