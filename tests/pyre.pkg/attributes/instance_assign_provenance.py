#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an instance with a value of its own reports the priority and the location of its own
setting
"""


def test() -> None:
    """
    Set the class trait in the store, give an instance a value of its own, and ask the instance
    where its value came from
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

    # set the class trait in the store directly, the way a configuration file does
    nameserver.insert(
        name="pyre.tests.attributes.base.t",
        value="changed",
        priority=nameserver.priority.user(),
        locator=pyre.tracking.simple("the test"),
    )
    # an instance
    b = base(name="b")
    # with a value of its own
    b.t = "own"
    # reports the priority of its own setting
    assert b.pyre_how("t").category == nameserver.priority.explicit.category
    # and its location, in this file
    assert str(b.pyre_where("t").source) == __file__

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
