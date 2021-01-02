#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2021 all rights reserved


def test():
    """
    Verify that we can control the global verbosity threshold
    """
    # access
    import journal

    # get the global state
    chronicler = journal.chronicler

    # verify that the verbosity level is at its default value
    assert chronicler.verbosity == 1
    # set it to some other value
    chronicler.verbosity = 5
    # verify the assignment sticks
    assert chronicler.verbosity == 5

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
