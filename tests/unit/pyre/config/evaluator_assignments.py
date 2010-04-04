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
    # create some assignments
    configurator.createAssignment(
        key="pyre.user.name", value="michael aïvázis", locator=None)
    configurator.createAssignment(
        key="pyre.user.email", value="michael.aivazis@orthologue.com", locator=None)
    configurator.createAssignment(
        key="pyre.user.affiliation", value="caltech", locator=None)

    # build a new evaluator
    evaluator = pyre.config.newEvaluator()
    # build the model
    print(" *** NYI!")
    # and return the managers
    return evaluator, configurator


# main
if __name__ == "__main__":
    test()


# end of file 
