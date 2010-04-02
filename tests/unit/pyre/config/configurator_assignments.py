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
    configurator.createAssignment(key="pyre.user.name", value="michael aïvázis")
    configurator.createAssignment(key="pyre.user.email", value="michael.aivazis@orthologue.com")
    configurator.createAssignment(key="pyre.user.affiliation", value="caltech")
    # check that they were created and inserted correctly
    assert list(map(str, configurator.events)) == [
        "{pyre.user.name <- michael aïvázis}",
        "{pyre.user.email <- michael.aivazis@orthologue.com}",
        "{pyre.user.affiliation <- caltech}",
        ]


# main
if __name__ == "__main__":
    test()


# end of file 
