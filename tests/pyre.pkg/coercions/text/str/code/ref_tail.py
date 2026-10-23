#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a str trait set to '{c.a}/tail', where the referent is unset, is unset
"""


def test() -> None:
    """
    Unset the referent, point the trait at it with a template, and read the trait
    """
    # access the framework
    import pyre

    # a component with a str trait
    class component(pyre.component):
        """a component with a str trait"""

        # the trait
        t = pyre.properties.str()
        # and its referent
        a = pyre.properties.str()

    # make an instance
    c = component(name="c")
    # unset the referent
    c.a = None
    # and point the trait at it
    c.t = "{c.a}/tail"
    # the setting took effect, at the rank of its source
    assert c.pyre_how(attribute="t").category == pyre.executive.priority.explicit.category
    # the trait is unset
    assert c.t is None

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
