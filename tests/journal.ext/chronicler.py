#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that the manager of the global state is available
    """
    # access
    from journal import libjournal

    # verify we have access to the global state
    chronicler = libjournal.chronicler

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
