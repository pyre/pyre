#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2023 all rights reserved


def test():
    """
    Exercise the simple use case with a wall clock timer
    """
    # externals
    import time
    # access the timer bindings
    from pyre.extensions.pyre.timers import WallTimer

    # make a timer
    t = WallTimer(name="tests.timer")
    # start it
    t.start()

    # take a nap
    time.sleep(.5)

    # stop the timer
    t.stop()

    # get the journal
    import journal
    # make a channel
    channel = journal.debug(name="pyre.timers")
    # activate it
    # channel.activate()
    # log the elapsed time
    channel.log(f"elapsed: {t.ms()}ms")

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
