#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Verify direct access to the configuration state
"""


def test():
    # access the package
    import pyre
    # and the configurator
    configurator = pyre.executive.configurator

    # create some assignments
    configurator["sample.user.name"] = "Michael Aïvázis"
    configurator["sample.user.name"] = "michael aïvázis"
    configurator["sample.user.email"] = "michael.aivazis@caltech.edu"
    configurator["sample.user.affiliation"] = "california institute of technology"
    configurator["sample.user.alias"] = "{sample.user.name}"

    # dump the contents of the model
    # configurator.dump()

    # check the variable bindings
    assert configurator["sample.user.name"] == "michael aïvázis"
    assert configurator["sample.user.email"] == "michael.aivazis@caltech.edu"
    assert configurator["sample.user.affiliation"] == "california institute of technology"
    assert configurator["sample.user.alias"] == configurator["sample.user.name"]

    # and return the managers
    return configurator


# main
if __name__ == "__main__":
    test()


# end of file 
