#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an assignment to an instance attribute gives the instance a value of its own, as with
python classes
"""


def test() -> None:
    """
    Make an instance, assign to it, and read it
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
    # give it a value of its own
    b.t = "own"
    # which it holds
    assert b.t == "own"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
