#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Check a few of the canonical X11 color names
    """
    # access the color map
    from journal.ANSI import ANSI

    # and the control sequence generator
    from journal.CSI import CSI

    # verify some colors
    assert ANSI.x11("normal") == CSI.reset()

    assert ANSI.x11("burlywood") == CSI.csi24(0xDE, 0xB8, 0x87)
    assert ANSI.x11("dark goldenrod") == CSI.csi24(0xB8, 0x86, 0x0B)
    assert ANSI.x11("dark khaki") == CSI.csi24(0xBD, 0xB7, 0x6B)
    assert ANSI.x11("dark orange") == CSI.csi24(0xFF, 0x8C, 0x00)
    assert ANSI.x11("dark sea green") == CSI.csi24(0x8F, 0xBC, 0x8F)
    assert ANSI.x11("firebrick") == CSI.csi24(0xB2, 0x22, 0x22)
    assert ANSI.x11("hot pink") == CSI.csi24(0xFF, 0x69, 0xB4)
    assert ANSI.x11("indian red") == CSI.csi24(0xCD, 0x5C, 0x5C)
    assert ANSI.x11("lavender") == CSI.csi24(0xE6, 0xE6, 0xFA)
    assert ANSI.x11("light green") == CSI.csi24(0x90, 0xEE, 0x90)
    assert ANSI.x11("light steel blue") == CSI.csi24(0xB0, 0xC4, 0xDE)
    assert ANSI.x11("light slate gray") == CSI.csi24(0x77, 0x88, 0x99)
    assert ANSI.x11("lime green") == CSI.csi24(0x32, 0xCD, 0x32)
    assert ANSI.x11("navajo white") == CSI.csi24(0xFF, 0xDE, 0xAD)
    assert ANSI.x11("olive drab") == CSI.csi24(0x6B, 0x8E, 0x23)
    assert ANSI.x11("peach puff") == CSI.csi24(0xFF, 0xDA, 0xB9)
    assert ANSI.x11("steel blue") == CSI.csi24(0x46, 0x82, 0xB4)

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
