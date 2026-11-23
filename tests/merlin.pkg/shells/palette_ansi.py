#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the palette of merlin draws its colors from a color terminal
"""


def test():
    """
    Build the palette on an ANSI terminal, and check its colors are escape sequences
    """
    # support
    from pyre.terminals.ANSI import ANSI
    from merlin.shells.Palette import Palette

    # a color terminal
    terminal = ANSI(name="palette_ansi")
    # build the palette on it
    palette = Palette(terminal=terminal)
    # the plain color ends any other
    assert palette.normal == terminal.reset(), repr(palette.normal)
    # and the color of projects is the terminal's steel blue
    assert palette.project == terminal.color("steel blue"), repr(palette.project)
    # which is an escape sequence
    assert palette.project.startswith("\x1b["), repr(palette.project)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
