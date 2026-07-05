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

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
