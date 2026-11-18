#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a socket pair whose process has a full descriptor table receives the bytes of a
message without its descriptors, that claiming them raises {ArrivalError}, and that the next
message arrives intact
"""

# externals
import errno
import os
import resource

# support
import pyre.ipc


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
    # make a pair of socket channels
    parent, child = pyre.ipc.newSocket().open()
    # and a pipe, whose end will travel
    reader, writer = os.pipe()
    # send a message along with the end
    parent.write(bytes=b"12345678", descriptors=[reader])
    # followed by a message without descriptors
    parent.write(bytes=b"next")

    # fill the descriptor table
    limits, fillers = fill()
    # carefully, so the table is emptied no matter what
    try:
        # the bytes of the first message arrive
        assert child.read(minlen=8, maxlen=8) == b"12345678"
        # but not its descriptor, so the claim
        try:
            # for it
            child.claim(count=1)
        # fails
        except pyre.ipc.exceptions.ArrivalError as error:
            # naming the channel
            assert error.channel is child
            # how many descriptors were sent
            assert error.expected == 1
            # how many arrived
            assert error.received == 0
            # and the limit that left no room for them
            assert error.limit == 64
            # which the message mentions
            assert "its limit is 64" in str(error), str(error)
        # anything else
        else:
            # is a failure
            assert False, "the claim found the missing descriptor"
        # nothing is left waiting to be claimed
        assert child.arrivals == []
        # and the next message arrives intact
        assert child.read(minlen=4, maxlen=4) == b"next"
    # whatever happened
    finally:
        # make room again
        empty(limits=limits, fillers=fillers)

    # clean up
    for descriptor in (reader, writer):
        # the pipe
        os.close(descriptor)
    # and the channels
    for channel in (parent, child):
        # one at a time
        channel.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
