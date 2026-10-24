#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that deleting an instance attribute makes the instance see its class again, as with python
classes
"""


def test() -> None:
    """
    Make an instance, give it a value, delete it, and read the instance
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
