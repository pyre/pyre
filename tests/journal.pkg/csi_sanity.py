#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


# verify we can build escape sequences correctly
def test():
    """
    Verify we can build escape sequences correctly
    """
    # get the modules
    from journal.CSI import CSI
    from journal.ASCII import ASCII

    # get the escape character
    esc = ASCII.ESC

    # verify the escape sequence generation routines build the correct strings
    assert CSI.reset() == f"{esc}[0m"
    assert CSI.csi3(code=35) == f"{esc}[0;35m"
    assert CSI.csi8(red=4, green=2, blue=3) == f"{esc}[38;5;175m"
    assert CSI.csi8_gray(gray=16) == f"{esc}[38;5;248m"
    assert CSI.csi24(red=0xff, green=0xbf, blue=0x00) == f"{esc}[38;2;255;191;0m"

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
