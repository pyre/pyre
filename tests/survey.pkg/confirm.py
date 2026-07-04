#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    A {Confirm} maps replies, and a blank line, onto a bool
    """
    # get the package and the input builtin
    import builtins
    import survey

    # an explicit no is false, whatever the default
    builtins.input = lambda prompt="": "n"
    assert survey.Confirm(message="ok", default=True).ask() is False

    # an explicit yes is true
    builtins.input = lambda prompt="": "yes"
    assert survey.Confirm(message="ok", default=False).ask() is True

    # a blank line takes the default
    builtins.input = lambda prompt="": ""
    assert survey.Confirm(message="ok", default=True).ask() is True

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
