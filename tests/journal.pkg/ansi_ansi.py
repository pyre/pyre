#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Check a few of the canonical ANSI color names
    """
    # access the color map
    from journal.ANSI import ANSI
    # and the control sequence generator
    from journal.CSI import CSI

    # verify the contents of the {ansi} color table
    # the reset sequence
    assert ANSI.ansi("normal") == CSI.reset()

    # regular colors
    assert ANSI.ansi("black") == CSI.csi3(code=30)
    assert ANSI.ansi("red") == CSI.csi3(code=31)
    assert ANSI.ansi("green") == CSI.csi3(code=32)
    assert ANSI.ansi("brown") == CSI.csi3(code=33)
    assert ANSI.ansi("blue") == CSI.csi3(code=34)
    assert ANSI.ansi("purple") == CSI.csi3(code=35)
    assert ANSI.ansi("cyan") == CSI.csi3(code=36)
    assert ANSI.ansi("light-gray") == CSI.csi3(code=37)

    # bright colors
    assert ANSI.ansi("dark-gray") == CSI.csi3(code=30, bright=True)
    assert ANSI.ansi("light-red") == CSI.csi3(code=31, bright=True)
    assert ANSI.ansi("light-green") == CSI.csi3(code=32, bright=True)
    assert ANSI.ansi("yellow") == CSI.csi3(code=33, bright=True)
    assert ANSI.ansi("light-blue") == CSI.csi3(code=34, bright=True)
    assert ANSI.ansi("light-purple") == CSI.csi3(code=35, bright=True)
    assert ANSI.ansi("light-cyan") == CSI.csi3(code=36, bright=True)
    assert ANSI.ansi("white") == CSI.csi3(code=37, bright=True)

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
