#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that {JOURNAL_DETAIL} sets the maximum detail level
    """
    # access
    import journal

    # check the level the environment asked for
    assert journal.detail() == 5, journal.detail()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
