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
    import pyre
    import survey

    # a plain terminal over in-memory streams reports as non-interactive; make it the one
    # terminal the prompts ride, forcing the numbered fallback
    from pyre.terminals.Plain import Plain

    pyre.executive.terminal = Plain(
        name="test.select.plain", istream=io.StringIO(), ostream=io.StringIO()
    )
    # the choices to offer
    options = ["red", "green", "blue"]

    # answer the numbered prompt with the second option
    builtins.input = lambda prompt="": "2"
    # swallow the menu it prints so a passing test stays silent
    with contextlib.redirect_stdout(io.StringIO()):
        # run the selection over the non-interactive terminal
        choice = survey.Select(message="pick", options=options).ask()
    # the fallback should have honored the reply
    assert choice == "green", choice

    # a buffer holding the {down arrow} escape sequence
    keystream = bytearray(b"\x1b[B")
    # a puller that walks that buffer one byte at a time
    pull = lambda: keystream.pop(0) if keystream else None
    # decoding {ESC [ B} should yield the down arrow
    assert survey.keys.decode(pull, pull).name == survey.keys.DOWN

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
