#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an instance that has read a trait keeps the value it read when its class changes, as
with a python cached property
"""


def test() -> None:
    """
    Make an instance, read its trait, assign to the class, and read the instance again
    """
    # access the framework
    import pyre

    # a component class with a trait
    class base(pyre.component, family="pyre.tests.attributes.base"):
        """a component class with a trait"""

        # the trait, with its class default
        t = pyre.properties.str(default="class")

    # an instance
    b = base(name="b")
    # that reads its trait
    assert b.t == "class"
    # change the class
    base.t = "changed"
    # the instance keeps what it read
    assert b.t == "class"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
