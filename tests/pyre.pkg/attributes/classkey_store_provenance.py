#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an instance that follows its class reports the priority and the location of the class
setting, since it only observes it
"""


def test() -> None:
    """
    Make an instance, set the key of the class trait in the store, and ask the instance where its
    value came from
    """
    # access the framework
    import pyre

    # the store
    nameserver = pyre.executive.nameserver

    # a component class with a trait
    class base(pyre.component, family="pyre.tests.attributes.base"):
        """a component class with a trait"""

        # the trait, with its class default
        t = pyre.properties.str(default="class")

    # an instance that follows its class
    b = base(name="b")
    # where the class setting comes from
    locator = pyre.tracking.simple("the test")
    # set the class trait in the store directly, the way a configuration file does
    nameserver.insert(
        name="pyre.tests.attributes.base.t",
        value="changed",
        priority=nameserver.priority.user(),
        locator=locator,
    )
    # the instance reports the priority of the class setting
    assert b.pyre_how("t").category == nameserver.priority.user.category
    # and its location
    assert b.pyre_where("t") is locator

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
