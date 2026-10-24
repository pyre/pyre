#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an assignment to a class attribute reaches a subclass, as with python classes
"""


def test() -> None:
    """
    Assign to the class, and read the subclass
    """
    # access the framework
    import pyre

    # a component class with a trait
    class base(pyre.component, family="pyre.tests.attributes.base"):
        """a component class with a trait"""

        # the trait, with its class default
        t = pyre.properties.str(default="class")

    # a subclass that says nothing about the trait
    class derived(base, family="pyre.tests.attributes.derived"):
        """a subclass that inherits the trait"""

    # change the class
    base.t = "changed"
    # the subclass sees the change
    assert derived.t == "changed"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
