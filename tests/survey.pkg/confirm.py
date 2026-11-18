#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A {Confirm} maps replies, and a blank line, onto a bool
    """
    # for scripting the replies
    import builtins

    # get the package
    import survey

    # feed an explicit no
    builtins.input = lambda prompt="": "n"
    # which is false whatever the default
    assert survey.Confirm(message="ok", default=True).ask() is False

    # feed an explicit yes
    builtins.input = lambda prompt="": "yes"
    # which is true
    assert survey.Confirm(message="ok", default=False).ask() is True

    # feed a blank line
    builtins.input = lambda prompt="": ""
    # which takes the default
    assert survey.Confirm(message="ok", default=True).ask() is True

    # an exhausted or closed input stream raises {EOFError}
    def exhausted(prompt=""):
        """
        Stand in for a reader that has hit the end of its input
        """
        # by saying so
        raise EOFError

    # feed it
    builtins.input = exhausted
    # which takes the default rather than crashing, whichever way it points
    assert survey.Confirm(message="ok", default=True).ask() is True
    # in both directions
    assert survey.Confirm(message="ok", default=False).ask() is False

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
