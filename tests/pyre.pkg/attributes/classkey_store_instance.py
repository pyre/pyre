#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a setting of the class key that bypasses the class reaches an existing instance, as with
python classes
"""


def test() -> None:
    """
    Make an instance, set the key of the class trait in the store, and read the instance
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

    # an instance made before the change
    b = base(name="b")
    # set the class trait in the store directly, the way a configuration file does
    nameserver.insert(
        name="pyre.tests.attributes.base.t",
        value="changed",
        priority=nameserver.priority.user(),
        locator=pyre.tracking.simple("the test"),
    )
    # the instance sees the change
    assert b.t == "changed"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
