#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that deleting an instance attribute set by the configuration makes the instance see its
class again
"""


def test() -> None:
    """
    Set the instance key in the store, delete the attribute, and read the instance
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
    # with a value set in the store, the way a configuration file does
    nameserver.insert(
        name="b.t",
        value="configured",
        priority=nameserver.priority.user(),
        locator=pyre.tracking.simple("the test"),
    )
    # that it gives up
    del b.t
    # so it sees the class again
    assert b.t == "class"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
