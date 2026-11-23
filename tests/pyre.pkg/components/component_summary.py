#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the summary of a component is its docstring, without the blank lines around it
"""


def test():
    """
    Declare a component with a docstring of two paragraphs, and check its summary
    """
    # access the framework
    import pyre

    # a component with a docstring in the expanded style
    class Thing(pyre.component, family="pyre.tests.things.summary"):
        """
        A thing

        That does things
        """

    # make one
    thing = Thing(name="thing")
    # build its summary
    summary = list(thing.pyre_showSummary(indent="  "))
    # and check it holds the two paragraphs, indented, and nothing around them
    assert summary == ["  A thing", "  ", "  That does things"], summary
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
