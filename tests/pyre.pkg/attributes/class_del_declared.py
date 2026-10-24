#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that deleting a class attribute of the class that declares the trait restores the declared
default
"""


def test() -> None:
    """
    Give the declaring class a value, delete it, and read the class
    """
    # access the framework
    import pyre

    # a component class with a trait
    class base(pyre.component, family="pyre.tests.attributes.base"):
        """a component class with a trait"""

        # the trait, with its class default
        t = pyre.properties.str(default="class")

    # give the class a value
    base.t = "changed"
    # that it gives up
    del base.t
    # so it holds the declared default again
    assert base.t == "class"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
