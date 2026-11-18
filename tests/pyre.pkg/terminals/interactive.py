#!/usr/bin/env python3
# -*- python -*-
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

    # and instantiate it
    terminal = Interactive(name="test.interactive")

    # it is a live terminal, so it offers raw input and cursor control
    assert callable(terminal.rawmode)
    # and reads keys
    assert callable(terminal.readkey)
    # cursor control emits the expected DEC private-mode sequences
    assert terminal.hideCursor() == "\x1b[?25l"
    # both ways
    assert terminal.showCursor() == "\x1b[?25h"
    # a rewind steps up over the frame, returns to the margin, and clears downward
    assert terminal.rewind(3) == "\x1b[3A\r\x1b[J"
    # a zero-height frame skips the cursor-up step
    assert terminal.rewind(0) == "\r\x1b[J"

    # but it is colorless, so every color request comes back empty
    assert terminal.color("red") == ""
    # named or numeric
    assert terminal.rgb("c02020") == ""
    # it renders nothing
    assert terminal.render(None) == ""
    # and has nothing to reset
    assert terminal.reset() == ""

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
