#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The evaluation of text drops its leading spaces and tabs, but its compilation does not; so
{pyre.calc.evaluation}, which compiles text before evaluating it, drops them itself
"""


def test() -> None:
    """
    Evaluate and compile text that starts with spaces and tabs
    """
    # text with leading and trailing whitespace
    text = " \t 2*3 "
    # evaluates
    assert eval(text) == 6
    # carefully
    try:
        # but does not compile
        compile(text, "<string>", "eval")
    # because of the indentation
    except IndentationError:
        # as expected
        pass
    # if it compiles
    else:
        # the evaluator no longer needs to drop the whitespace, so say so
        assert False, "text with leading whitespace now compiles"
    # without its leading spaces and tabs, it compiles
    assert eval(compile(text.lstrip(" \t"), "<string>", "eval")) == 6

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
