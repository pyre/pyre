#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    An ANSI terminal renders named colors as truecolor escapes through {chroma}
    """
    # get the framework
    import pyre

    # there is nothing to check when the color bindings were not built into this configuration
    if pyre.libpyre is None:
        # so quietly succeed
        return

    # make an ANSI terminal
    from pyre.terminals.ANSI import ANSI

    term = ANSI(name="test.ansi")

    # it is a color terminal
    assert term.chromatic is True
    # a named color renders as a 24-bit truecolor escape
    assert term.color("red") == "\x1b[38;2;255;0;0m"
    # alias spellings resolve too, since the palette is complete
    assert term.color("fuchsia") != ""
    # an unknown name renders nothing
    assert term.color("not-a-color") == ""
    # the reset sequence is the canonical one
    assert term.reset() == "\x1b[0m"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
