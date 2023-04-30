#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Verify that we can instantiate a cpu timer
    """
    # access the timer bindings
    from pyre.extensions.pyre.timers import ProcessTimer

    # make a timer
    t = ProcessTimer(name="tests.timer")
    # verify its name
    assert t.name == "tests.timer"

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
