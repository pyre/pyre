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

    # the nodes
    name = pyre.calc.newNode(value="Michael Aïvázis")
    email = pyre.calc.newNode(value="aivazis@caltech.edu")
    signature = pyre.calc.newNode(value=pyre.calc.expression(
            formula="{user.name}+' -- '+{user.email}", model=model))
    
    # register the nodes
    model.register(name="user.name", node=name)
    model.register(name="user.email", node=email)
    model.register(name="user.signature", node=signature)

    # check the signature
    assert signature.value == "Michael Aïvázis -- aivazis@caltech.edu"

    return


# main
if __name__ == "__main__":
    test()


# end of file 
