#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


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

    assert ANSI.x11("burlywood") == CSI.csi24(0xde, 0xb8, 0x87)
    assert ANSI.x11("dark goldenrod") == CSI.csi24(0xb8, 0x86, 0x0b)
    assert ANSI.x11("dark khaki") == CSI.csi24(0xbd, 0xb7, 0x6b)
    assert ANSI.x11("dark orange") == CSI.csi24(0xff, 0x8c, 0x00)
    assert ANSI.x11("dark sea green") == CSI.csi24(0x8f, 0xbc, 0x8f)
    assert ANSI.x11("firebrick") == CSI.csi24(0xb2, 0x22, 0x22)
    assert ANSI.x11("hot pink") == CSI.csi24(0xff, 0x69, 0xb4)
    assert ANSI.x11("indian red") == CSI.csi24(0xcd, 0x5c, 0x5c)
    assert ANSI.x11("lavender") == CSI.csi24(0xe6, 0xe6, 0xfa)
    assert ANSI.x11("light green") == CSI.csi24(0x90, 0xee, 0x90)
    assert ANSI.x11("light steel blue") == CSI.csi24(0xb0, 0xc4, 0xde)
    assert ANSI.x11("light slate gray") == CSI.csi24(0x77, 0x88, 0x99)
    assert ANSI.x11("lime green") == CSI.csi24(0x32, 0xcd, 0x32)
    assert ANSI.x11("navajo white") == CSI.csi24(0xff, 0xde, 0xad)
    assert ANSI.x11("olive drab") == CSI.csi24(0x6b, 0x8e, 0x23)
    assert ANSI.x11("peach puff") == CSI.csi24(0xff, 0xda, 0xb9)
    assert ANSI.x11("steel blue") == CSI.csi24(0x46, 0x82, 0xb4)

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
