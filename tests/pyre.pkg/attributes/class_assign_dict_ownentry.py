#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an assignment to a class dictionary reaches the entries of an existing instance that are
not its own, as with python classes
"""


def test() -> None:
    """
    Give an instance an entry of its own in the store, assign new values to the class, and read the
    instance
    """
    # access the framework
    import pyre

    # the store
    nameserver = pyre.executive.nameserver

    # a component class with a dictionary
    class base(pyre.component, family="pyre.tests.attributes.base"):
        """a component class with a dictionary"""

        # the dictionary, with its class default
        t = pyre.properties.dict(schema=pyre.properties.int(), default={"a": 1, "b": 2})

    # an instance
    b = base(name="b")
    # with an entry of its own, set the way a configuration file does
    nameserver.insert(
        name="b.t.a",
        value=5,
        priority=nameserver.priority.user(),
        locator=pyre.tracking.simple("the test"),
    )
    # change the values of the class
    base.t = {"a": 10, "b": 20}
    # the instance keeps its own entry and sees the new value of the other one
    assert dict(b.t) == {"a": 5, "b": 20}

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
