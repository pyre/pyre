#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a mill returns to its margin, however deep it was indented
"""


def test():
    """
    Indent a mill a few levels, return it to its margin, and check where the next line goes
    """
    # get the package
    import pyre

    # instantiate a weaver
    weaver = pyre.weaver.weaver(name="margin")
    # that speaks SQL
    weaver.language = "sql"
    # access its mill
    mill = weaver.language

    # indent a few levels
    mill.indent(increment=3)
    # check that lines are indented
    assert mill.place("text") != "text", mill.place("text")
    # return to the margin
    mill.margin()
    # and check that lines start there
    assert mill.place("text") == "text", mill.place("text")

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
