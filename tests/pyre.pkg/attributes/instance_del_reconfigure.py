#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an instance that gave up its value takes a later setting from the configuration
"""


def test() -> None:
    """
    Give an instance a value, delete it, set its key in the store, and read the instance
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

    # an instance
    b = base(name="b")
    # with a value of its own
    b.t = "own"
    # that it gives up
    del b.t
    # a later setting in the store, the way a configuration file does
    nameserver.insert(
        name="b.t",
        value="configured",
        priority=nameserver.priority.user(),
        locator=pyre.tracking.simple("the test"),
    )
    # reaches the instance
    assert b.t == "configured"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
