#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Check a few of the canonical greay tones
    """
    # access the color map
    from journal.ANSI import ANSI

    # and the control sequence generator
    from journal.CSI import CSI

    # verify the contents of the {gray} color table
    # the reset sequence
    assert ANSI.gray("normal") == CSI.reset()

    # verify the contents of the {gray} color table; these are the canonical X11 gray values
    assert ANSI.gray("gray10") == CSI.csi24(red=0x1A, green=0x1A, blue=0x1A)
    assert ANSI.gray("gray30") == CSI.csi24(red=0x4D, green=0x4D, blue=0x4D)
    assert ANSI.gray("gray41") == CSI.csi24(red=0x69, green=0x69, blue=0x69)
    assert ANSI.gray("gray50") == CSI.csi24(red=0x7F, green=0x7F, blue=0x7F)
    assert ANSI.gray("gray66") == CSI.csi24(red=0xA8, green=0xA8, blue=0xA8)
    assert ANSI.gray("gray75") == CSI.csi24(red=0xBF, green=0xBF, blue=0xBF)

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
