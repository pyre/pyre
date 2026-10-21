#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
The evaluation of text sees the builtins its globals provide under {__builtins__}, and all of
them when there is no such entry; a builtin it can't see raises a {NameError} that carries the
name; {pyre.calc.evaluation} relies on all of this to restrict what settings may use
"""


def test() -> None:
    """
    Evaluate text with and without a restricted set of builtins
    """
    # globals without builtins
    context = {}
    # see all of them
    assert eval("len('abc')", context) == 3
    # because the interpreter added them
    assert "__builtins__" in context

    # globals with a few builtins
    context = {"__builtins__": {"abs": abs}}
    # see those
    assert eval("abs(-1)", context) == 1
    # carefully
    try:
        # but not the others
        eval("len('abc')", context)
    # they are undefined names
    except NameError as error:
        # that carry the name
        assert error.name == "len", error.name
    # if the others are visible
    else:
        # say so
        assert False, "a restricted evaluation saw 'len'"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
