#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a marshaler whose process has a full descriptor table consumes a message that
carries a channel, raises {ArrivalError}, and receives the next message intact
"""

# externals
import errno
import os
import resource

# support
import pyre.ipc

# the channel that travels
from pyre.ipc.File import File


def fill():
    """
    Lower the limit on the number of open descriptors and open as many as it allows
    """
    # get the current limits
    limits = resource.getrlimit(resource.RLIMIT_NOFILE)
    # lower the soft one, so the table is quick to fill
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, limits[1]))
    # the descriptors that fill the table
    fillers = []
    # until there is no more room
    while True:
        # carefully
        try:
            # open one more
            fillers.append(os.open(os.devnull, os.O_RDONLY))
        # when the table is full
        except OSError as error:
            # make sure that is what happened
            assert error.errno == errno.EMFILE, error
            # and stop
            break
    # hand off what must be undone
    return limits, fillers


def empty(limits, fillers):
    """
    Close the {fillers} and restore the {limits}
    """
    # close the fillers
    for descriptor in fillers:
        # one at a time
        os.close(descriptor)
    # and restore the limits
    resource.setrlimit(resource.RLIMIT_NOFILE, limits)
    # all done
    return


def test():
    # the channel the messages travel over
    parent, child = pyre.ipc.newSocket().open()
    # and the marshaler
    pickler = pyre.ipc.newPickler()

    # make a channel over a file with no name
    payload = File.temporary()
    # send it inside a message
    pickler.send(item={"payload": payload}, channel=parent)
    # followed by a message without channels
    pickler.send(item="next", channel=parent)

    # fill the descriptor table
    limits, fillers = fill()
    # carefully, so the table is emptied no matter what
    try:
        # the first message
        try:
            # cannot be received
            pickler.recv(channel=child)
        # without its descriptor
        except pyre.ipc.exceptions.ArrivalError as error:
            # which was sent
            assert error.expected == 1
            # but did not arrive
            assert error.received == 0
        # anything else
        else:
            # is a failure
            assert False, "the message arrived with its channel"
        # nothing is left waiting to be claimed
        assert child.arrivals == []
        # and the next message arrives intact
        assert pickler.recv(channel=child) == "next"
    # whatever happened
    finally:
        # make room again
        empty(limits=limits, fillers=fillers)

    # clean up
    for channel in (payload, parent, child):
        # one channel at a time
        channel.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
