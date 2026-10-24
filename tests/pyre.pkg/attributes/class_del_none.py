#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that deleting a class attribute the class has no value for is an error, as with python
classes
"""


def test() -> None:
    """
    Delete an attribute of a subclass that has no value of its own
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

    # attempt to
    try:
        # delete the attribute
        del derived.t
        # which should be unreachable
        assert False, "unreachable"
    # if it fails as expected
    except AttributeError:
        # all good
        pass

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
