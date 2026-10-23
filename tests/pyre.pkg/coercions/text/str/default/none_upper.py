#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a str trait whose default is the text 'NONE' is unset
"""


def test() -> None:
    """
    Declare a str trait that defaults to the text 'NONE', make an instance, and read it
    """
    # access the framework
    import pyre

    # a component with a str trait
    class component(pyre.component):
        """a component with a str trait"""

        # the trait
        t = pyre.properties.str()
        # whose default is the text 'NONE'
        t.default = "NONE"

    # make an instance
    c = component(name="c")
    # the trait is unset
    assert c.t is None

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
