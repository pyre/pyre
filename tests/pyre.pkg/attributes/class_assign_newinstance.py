#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that an assignment to a class attribute reaches an instance made after it, as with python
classes
"""


def test() -> None:
    """
    Assign to the class, make an instance, and read it
    """
    # access the framework
    import pyre

    # a component class with a trait
    class base(pyre.component, family="pyre.tests.attributes.base"):
        """a component class with a trait"""

        # the trait, with its class default
        t = pyre.properties.str(default="class")

    # change the class
    base.t = "changed"
    # an instance made after the change sees it
    assert base(name="b").t == "changed"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
