#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


"""
Check that configurations can be populated correctly
"""


def test():
    import pyre.config
    # build a new configurator
    configuration = pyre.config.newConfiguration()
    # create some assignments
    configuration.newAssignment(
        key=("pyre", "user", "name"), value="michael aïvázis", locator=None)
    configuration.newAssignment(
        key=("pyre", "user", "email"), value="michael.aivazis@orthologue.com", locator=None)
    configuration.newAssignment(
        key=("pyre", "user", "affiliation"), value="caltech", locator=None)
    # check that they were created and inserted correctly
    assert list(map(str, configuration.events)) == [
        "{None: pyre.user.name <- michael aïvázis}",
        "{None: pyre.user.email <- michael.aivazis@orthologue.com}",
        "{None: pyre.user.affiliation <- caltech}",
        ]


# main
if __name__ == "__main__":
    test()


# end of file 
