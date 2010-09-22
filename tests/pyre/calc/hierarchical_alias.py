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
    model["user.signature"] = "{user.name}+' -- '+{user.email}"
    # check the signature
    assert model["user.signature"].value == "Michael Aïvázis -- aivazis@caltech.edu"

    # case 1: canonical does not exist, alias does not exist
    model.alias(alias="author.affiliation", canonical="user.affiliation")
    model["user.affiliation"] = "California Institute of Technology"
    assert model["author.affiliation"].value == model["user.affiliation"].value

    # case 2: canonical exists, alias does not
    model.alias(alias="author.signature", canonical="user.signature")
    # check the signature
    assert model["author.signature"].value == model["user.signature"].value

    # case 3: canonical does not exist, alias does
    model["author.telephone"] = "+1 626.395.3424"
    model.alias(alias="author.telephone", canonical="user.telephone")
    assert model["author.telephone"].value == model["user.telephone"].value

    # case 4: both are preëxisting nodes
    model["author.name"] = "TBD"
    model.alias(alias="author.name", canonical="user.name")
    assert model["author.name"].value == model["user.name"].value

    return


# main
if __name__ == "__main__":
    test()


# end of file 
