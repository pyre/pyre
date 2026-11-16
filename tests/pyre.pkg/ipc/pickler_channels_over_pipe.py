#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a message holding a channel cannot be sent over a pipe channel, which carries bytes
only
"""


def test():
    # access the package
    import pyre.ipc

    # the channel the message would travel over
    parent, child = pyre.ipc.newPipe().open()
    # and the channel inside the message
    passenger = pyre.ipc.newSocket().open()
    # carefully
    try:
        # attempt to send it
        pyre.ipc.newPickler().send(item={"channel": passenger.child}, channel=parent)
    # the pipe refuses
    except pyre.ipc.exceptions.CarriageError as error:
        # and says so
        assert error.channel is parent
    # anything else
    else:
        # is a failure
        assert False, "a channel travelled over a pipe"

    # clean up
    for channel in (parent, child, *passenger):
        # one channel at a time
        channel.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
