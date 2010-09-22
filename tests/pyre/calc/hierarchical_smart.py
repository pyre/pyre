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

    return


# main
if __name__ == "__main__":
    test()


# end of file 
