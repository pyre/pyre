#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    An interactive terminal has cursor control and raw input, but renders no color
    """
    # get the framework
    import pyre

    # make an interactive terminal
    from pyre.terminals.Interactive import Interactive

    term = Interactive(name="test.interactive")

    # it is a live terminal, so it offers raw input and cursor control
    assert callable(term.rawmode)
    assert callable(term.readkey)
    # cursor control emits the expected DEC private-mode sequences
    assert term.hideCursor() == "\x1b[?25l"
    assert term.showCursor() == "\x1b[?25h"
    # a rewind steps up over the frame, returns to the margin, and clears downward
    assert term.rewind(3) == "\x1b[3A\r\x1b[J"
    # a zero-height frame skips the cursor-up step
    assert term.rewind(0) == "\r\x1b[J"

    # but it is colorless, so every color request comes back empty
    assert term.color("red") == ""
    assert term.rgb("c02020") == ""
    assert term.render(None) == ""
    assert term.reset() == ""

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
