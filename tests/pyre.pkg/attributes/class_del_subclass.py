#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that deleting a class attribute of a subclass makes it see its parent again, as with python
classes
"""


def test() -> None:
    """
    Give a subclass a value, delete it, and read the subclass
    """
    # access the framework
    import pyre

    # a component class with a trait
    class base(pyre.component, family="pyre.tests.attributes.base"):
        """a component class with a trait"""

        # the trait, with its class default
        t = pyre.properties.str(default="class")

    # a subclass
    class derived(base, family="pyre.tests.attributes.derived"):
        """a subclass that inherits the trait"""

    # give the subclass a value of its own
    derived.t = "own"
    # that it gives up
    del derived.t
    # so it sees its parent again
    assert derived.t == "class"
    # and follows its later changes
    base.t = "changed"
    # as with python classes
    assert derived.t == "changed"

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
