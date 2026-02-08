#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


# support
import pyre
import journal
import time


# the driver
def test():
    """
    A progress bar test driver
    """
    # make a channel
    channel = journal.debug("pyre.shells.progress")
    # if the channel is not active
    if not channel:
        # skip this test
        return 0

    # otherwise,make a bar
    bar = pyre.shells.progress(name="bar")
    # set up the number of frames
    frames = 1000
    # go through them
    for frame in range(frames + 1):
        # update the bar
        bar.update(p=frame / frames)
        # sleep
        time.sleep(0.01)
    # all done
    return 0


# bootstrap
if __name__ == "__main__":
    # drive
    status = test()
    # and share
    raise SystemExit(status)


# end of file
