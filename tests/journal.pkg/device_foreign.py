#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def test() -> None:
    """
    Verify that no device of the pure python journal is foreign
    """
    # access
    import journal

    # the stock devices are native
    assert journal.trash().foreign is False
    assert journal.splitter().foreign is False

    # all done
    return


# main
if __name__ == "__main__":
    # skip the bindings, so the pure python implementation is exercised
    journal_no_libjournal = True
    # run the test
    test()


# end of file
