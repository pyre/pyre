#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a trait set by the user to a reference to a component that does not exist yet survives
the instantiation of its own component, and sees the value once the referent exists
"""


def test():
    """
    Set a trait to a reference to the trait of a later component, make the two instances in
    order, and read the reference
    """
    # access the framework
    import pyre

    # and the nameserver
    nameserver = pyre.executive.nameserver

    # set a trait to a reference to a component that does not exist yet, the way the command
    # line does with --early.label={late.title}
    nameserver.insert(
        name="early.label",
        value="{late.title}",
        priority=nameserver.priority.command(),
        locator=None,
    )

    # the component whose trait refers forward
    class referrer(pyre.component):
        """a component with a trait the user points at a later component"""

        # the trait that holds the reference
        label = pyre.properties.str(default="none of the above")

    # the component that is referred to
    class referent(pyre.component):
        """a component whose trait is referred to before it exists"""

        # the trait that is referred to
        title = pyre.properties.str(default="hello")

    # make the instance that refers forward, before its referent exists
    early = referrer(name="early")
    # make its referent
    late = referent(name="late")
    # the referent has its default
    assert late.title == "hello"
    # and the reference sees it
    assert early.label == "hello"

    # all done
    return early, late


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
