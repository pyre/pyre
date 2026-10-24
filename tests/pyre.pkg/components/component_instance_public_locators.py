#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify access to component traits and their meta-data
"""

# support
import pyre


# declare a public component
class public(pyre.component, family="sample.publiclocator"):
    """a public component"""

    # traits
    p = pyre.properties.str(default="p")


def test():
    # instantiate publicly
    c = public(name="c")
    # ask for the instance locator
    loc = c.pyre_where()
    # check that it is correct
    assert loc.source.endswith("component_instance_public_locators.py")
    assert loc.line == 27  # the line that made the instance
    assert loc.function == "test"  # in this function

    # ask for the trait value and verify it is the default
    assert c.p == "p"
    # ask for its locator; the value came from the class, so it is where the class was declared
    loc = c.pyre_where("p")
    # check it is correct
    assert loc.source.endswith("component_instance_public_locators.py")
    assert loc.line == 18  # the line that declared the class
    assert loc.function == "<module>"  # at the top level of this file

    # set it
    c.p = "q"
    # verify the setting worked
    assert c.p == "q"
    # ask for its locator
    loc = c.pyre_where("p")
    # check it is correct
    assert loc.source.endswith("component_instance_public_locators.py")
    assert loc.line == 45  # the line that set the trait
    assert loc.function == "test"  # in this function

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
