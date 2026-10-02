#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test():
    """
    Verify that {JOURNAL_DECOR} sets the decoration level
    """
    # access
    import journal

    # check the level the environment asked for
    assert journal.decor() == 3, journal.decor()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
