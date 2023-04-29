#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Make sure we can instantiate a wall clock timer
    """
    # access the timer bindings
    from pyre.extensions.pyre.timers import WallTimer

    # make a timer
    t = WallTimer(name="tests.timer")
    # verify its name
    assert t.name == "tests.timer"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
