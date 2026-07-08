#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A {Select} honors a reply through its numbered fallback, and takes its default when the input
    stream is exhausted
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

    # an exhausted or closed input stream raises {EOFError}
    def _eof(prompt=""):
        # stand in for a reader that has hit end-of-input
        raise EOFError

    builtins.input = _eof
    # so the numbered fallback settles on its default rather than looping or crashing
    with contextlib.redirect_stdout(io.StringIO()):
        # run the selection with no answer available
        settled = survey.Select(message="pick", options=options, default="blue").ask()
    # the default should have carried the day
    assert settled == "blue", settled

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
