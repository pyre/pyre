#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A {Select} honors a reply through its numbered fallback, and its key decoder reads arrows
    """
    # get the package and a few helpers
    import builtins
    import contextlib
    import io
    import survey

    # a console over in-memory streams reports as non-interactive, forcing the numbered fallback
    streams = survey.Console(istream=io.StringIO(), ostream=io.StringIO())
    options = ["red", "green", "blue"]

    # answer the numbered prompt with the second option, swallowing the menu it prints
    builtins.input = lambda prompt="": "2"
    with contextlib.redirect_stdout(io.StringIO()):
        choice = survey.Select(message="pick", options=options, console=streams).ask()
    assert choice == "green", choice

    # and the key decoder turns an escape sequence into the arrow it names
    keystream = bytearray(b"\x1b[B")
    pull = lambda: keystream.pop(0) if keystream else None
    assert survey.keys.decode(pull, pull).name == survey.keys.DOWN

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
