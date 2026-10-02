#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that the global decoration, detail and margin settings of the bindings can be set and
    reported through the same calls
    """
    # get the library
    import journal.ext.journal as libjournal

    # set the decoration level
    libjournal.decor(2)
    # and check that it is reported back
    assert libjournal.decor() == 2
    # set the maximum detail level
    libjournal.detail(3)
    # and check that it is reported back
    assert libjournal.detail() == 3
    # set the margin
    libjournal.margin(">> ")
    # and check that it is reported back
    assert libjournal.margin() == ">> "

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
