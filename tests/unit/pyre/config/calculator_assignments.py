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
    import pyre
    # build an executive
    executive = pyre.executive()
    # build a new configurator
    configurator = executive.configurator
    # build a new calculator
    calculator = executive.calculator

    # create some assignments
    configurator.recordAssignment(
        key="pyre.user.name", value="Michael Aïvázis", locator=None)
    configurator.recordAssignment(
        key="pyre.user.name", value="michael aïvázis", locator=None)
    configurator.recordAssignment(
        key="pyre.user.email", value="michael.aivazis@caltech.edu", locator=None)
    configurator.recordAssignment(
        key="pyre.user.affiliation",
        value="california institute of technology", locator=None)
    configurator.recordAssignment(
        key="pyre.user.alias", value="{pyre.user.name}", locator=None)

    # build the model
    configurator.configure(executive, priority=executive.USER_CONFIGURATION)

    # check the variable bindings
    assert calculator["pyre.user.name"] == "michael aïvázis"
    assert calculator["pyre.user.email"] == "michael.aivazis@caltech.edu"
    assert calculator["pyre.user.affiliation"] == "california institute of technology"
    assert calculator["pyre.user.alias"] == calculator["pyre.user.name"]

    # and return the managers
    return calculator, configurator


# main
if __name__ == "__main__":
    test()


# end of file 
