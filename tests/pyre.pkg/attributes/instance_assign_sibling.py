#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an assignment to an instance attribute leaves the other instances alone, as with python
classes
"""


def test() -> None:
    """
    Make two instances, assign to one, and read the other
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
    # and its sibling
    sibling = base(name="sibling")
    # give the first one a value of its own
    b.t = "own"
    # the other one still sees the class
    assert sibling.t == "class"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
