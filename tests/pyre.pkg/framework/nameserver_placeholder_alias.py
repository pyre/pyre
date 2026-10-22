#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a global setting merges into a trait name that was only referred to before its
component existed
"""


def test():
    """
    Set a trait by its short name, refer to it by its full name, then make the instance with
    global aliases, and check that the trait and the reference both see the setting
    """
    # access the package
    import pyre

    # and the nameserver
    nameserver = pyre.executive.nameserver

    # set a trait by its short name, the way the command line does with --title=x
    nameserver.insert(name="title", value="x", priority=nameserver.priority.command(), locator=None)
    # and refer to it by its full name, the way --late.label={late.title} does
    nameserver.insert(
        name="late.label",
        value="{late.title}",
        priority=nameserver.priority.command(),
        locator=None,
    )

    # a component with the two traits
    class component(pyre.component):
        """a component whose traits refer to each other"""

        # the trait that is set by its short name
        title = pyre.properties.str(default="hello")
        # and the one that refers to it
        label = pyre.properties.str()

    # make the instance, merging the global settings into its scope
    c = component(name="late", globalAliases=True)
    # the trait gets the global setting
    assert c.title == "x"
    # and the reference sees it
    assert c.label == "x"

    # all done
    return c


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
