#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an instance that has read a trait reports where the value it read came from, even after
its class changes
"""


def test() -> None:
    """
    Make an instance, read its trait, set the key of the class trait in the store, and ask the
    instance where its value came from
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
    # that reads its trait
    assert b.t == "class"
    # set the class trait in the store directly, the way a configuration file does
    nameserver.insert(
        name="pyre.tests.attributes.base.t",
        value="changed",
        priority=nameserver.priority.user(),
        locator=pyre.tracking.simple("the test"),
    )
    # the instance reports the provenance of what it read, the default of its class
    assert b.pyre_how("t").category == nameserver.priority.defaults.category
    # which is where the class was declared
    assert b.pyre_where("t") is base.pyre_locator

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
