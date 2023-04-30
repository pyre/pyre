#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


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

    # verify the contents of the {gray} color table
    assert ANSI.gray("gray10") == CSI.csi24(red=0x19, green=0x19, blue=0x19)
    assert ANSI.gray("gray30") == CSI.csi24(red=0x4c, green=0x4c, blue=0x4c)
    assert ANSI.gray("gray41") == CSI.csi24(red=0x69, green=0x69, blue=0x69)
    assert ANSI.gray("gray50") == CSI.csi24(red=0x80, green=0x80, blue=0x80)
    assert ANSI.gray("gray66") == CSI.csi24(red=0xa9, green=0xa9, blue=0xa9)
    assert ANSI.gray("gray75") == CSI.csi24(red=0xbe, green=0xbe, blue=0xbe)

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
