#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that the global decoration, detail and margin settings of the pure python implementation can be set and
    reported through the same calls
    """
    # get the journal
    import journal

    # set the decoration level
    journal.decor(2)
    # and check that it is reported back
    assert journal.decor() == 2
    # set the maximum detail level
    journal.detail(3)
    # and check that it is reported back
    assert journal.detail() == 3
    # set the margin
    journal.margin(">> ")
    # and check that it is reported back
    assert journal.margin() == ">> "

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
