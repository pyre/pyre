#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that we can detect ANSI compatible terminals correctly
    """
    # for the command line
    import sys
    # access the color map
    from journal.ANSI import ANSI

    # pull the expected value from the command line
    expectation = bool(int(sys.argv[1])) if len(sys.argv) > 1 else True
    # ask the color map
    observation = ANSI.compatible()

    # verify that the two match
    assert expectation == observation

    # all done
    return


# main
if __name__ == "__main__":
    # prohibit the journal bindings
    journal_no_libjournal = True
    # run the test
    test()


# end of file
