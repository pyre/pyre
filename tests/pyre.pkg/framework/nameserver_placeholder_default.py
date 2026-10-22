#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a trait whose name was only referred to before its component existed gets its
default
"""


def test():
    """
    Refer to a trait of an instance that does not exist yet, then make the instance, and check
    that the trait and the reference both see the default
    """
    # access the package
    import pyre

    # and the nameserver
    nameserver = pyre.executive.nameserver

    # a setting refers to a trait of an instance nobody has made yet, the way the command line
    # does with --early.label={early.title}
    nameserver.insert(
        name="early.label",
        value="{early.title}",
        priority=nameserver.priority.command(),
        locator=None,
    )

    # a component with the two traits
    class component(pyre.component):
        """a component whose traits refer to each other"""

        # the trait that is referred to
        title = pyre.properties.str(default="hello")
        # and the one that refers to it
        label = pyre.properties.str()

    # make the instance
    c = component(name="early")
    # the trait that was only referred to gets its default
    assert c.title == "hello"
    # and the reference sees it
    assert c.label == "hello"

    # all done
    return c


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
