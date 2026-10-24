#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that deleting an attribute of an instance without a name makes it see its class again, as
with python classes
"""


def test() -> None:
    """
    Make an instance without a name, give it a value, delete it, and read the instance
    """
    # access the framework
    import pyre

    # a component class with a trait
    class base(pyre.component, family="pyre.tests.attributes.base"):
        """a component class with a trait"""

        # the trait, with its class default
        t = pyre.properties.str(default="class")

    # an instance without a name
    b = base()
    # with a value of its own
    b.t = "own"
    # that it gives up
    del b.t
    # so it sees the class again
    assert b.t == "class"
    # and follows its later changes
    base.t = "changed"
    # as with python classes
    assert b.t == "changed"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
