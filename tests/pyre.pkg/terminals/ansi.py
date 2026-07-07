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
    # a 24-bit color also renders from a hex string or an integer, with an optional "#"
    assert term.rgb("c02020") == "\x1b[38;2;192;32;32m"
    assert term.rgb("#c02020") == "\x1b[38;2;192;32;32m"
    assert term.rgb(0xC02020) == "\x1b[38;2;192;32;32m"
    # an invalid hex code renders nothing
    assert term.rgb("nothex") == ""
    # the reset sequence is the canonical one
    assert term.reset() == "\x1b[0m"
    # cursor control emits the expected DEC private-mode sequences
    assert term.hideCursor() == "\x1b[?25l"
    assert term.showCursor() == "\x1b[?25h"
    # a rewind steps up over the frame, returns to the margin, and clears downward
    assert term.rewind(3) == "\x1b[3A\r\x1b[J"
    # a zero-height frame skips the cursor-up step
    assert term.rewind(0) == "\r\x1b[J"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
