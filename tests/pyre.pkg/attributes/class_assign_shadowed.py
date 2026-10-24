#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an assignment to a class attribute does not reach an instance with a value of its own, as
with python classes
"""


def test() -> None:
    """
    Make an instance, give it a value, assign to the class, and read the instance
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
    # with a value of its own
    b.t = "own"
    # change the class
    base.t = "changed"
    # the instance keeps its own value
    assert b.t == "own"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
