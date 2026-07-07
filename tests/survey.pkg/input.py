#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    An {Input} returns what the user typed, and its default on a blank reply
    """
    # get the package and the input builtin
    import builtins
    import survey

    # feed a typed reply
    builtins.input = lambda prompt="": "hello"
    # which should come back verbatim
    assert survey.Input(message="name", default="anon").ask() == "hello"

    # feed a blank reply
    builtins.input = lambda prompt="": ""
    # which should fall back to the default
    assert survey.Input(message="name", default="anon").ask() == "anon"

    # an exhausted or closed input stream raises {EOFError}
    def _eof(prompt=""):
        # stand in for a reader that has hit end-of-input
        raise EOFError

    builtins.input = _eof
    # which is treated as a blank reply, so the default stands
    assert survey.Input(message="name", default="anon").ask() == "anon"
    # and with no default, it comes back as the empty string rather than crashing
    assert survey.Input(message="name").ask() == ""

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
