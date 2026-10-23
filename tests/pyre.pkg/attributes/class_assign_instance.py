#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an assignment to a class attribute reaches an existing instance, as with python classes
"""


def test() -> None:
    """
    Make an instance, assign to the class, and read the instance
    """
    # access the framework
    import pyre

    # a component class with a trait
    class base(pyre.component, family="pyre.tests.attributes.base"):
        """a component class with a trait"""

        # the trait, with its class default
        t = pyre.properties.str(default="class")

    # an instance made before the change
    b = base(name="b")
    # change the class
    base.t = "changed"
    # the instance sees the change, as an instance of a python class would
    assert b.t == "changed"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
