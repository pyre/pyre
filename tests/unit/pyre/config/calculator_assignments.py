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
    import pyre.config
    # build a new configurator
    configurator = pyre.config.newConfigurator()
    # build a new calculator
    calculator = pyre.config.newCalculator()

    # create some assignments
    configurator.createAssignment(
        key="pyre.user.name", value="Michael Aïvázis", locator=None)
    configurator.createAssignment(
        key="pyre.user.name", value="michael aïvázis", locator=None)
    configurator.createAssignment(
        key="pyre.user.email", value="michael.aivazis@caltech.edu", locator=None)
    configurator.createAssignment(
        key="pyre.user.affiliation",
        value="california institute of technology", locator=None)
    configurator.createAssignment(
        key="pyre.user.alias", value="{pyre.user.name}", locator=None)

    # build the model
    configurator.populate(calculator)

    # dump the model
    calculator._dump()
    # and return the managers
    return calculator, configurator


# main
if __name__ == "__main__":
    test()


# end of file 
