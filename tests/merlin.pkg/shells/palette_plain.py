#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the palette of merlin works on a terminal without colors, where it has none
"""


def test():
    """
    Build the palette on a plain terminal, and check that every color is empty
    """
    # support
    from pyre.terminals.Plain import Plain
    from merlin.shells.Palette import Palette

    # build the palette on a terminal without colors
    palette = Palette(terminal=Plain(name="palette_plain"))
    # and check that none of its colors emits anything
    assert (palette.normal, palette.project, palette.library) == ("", "", ""), palette
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
