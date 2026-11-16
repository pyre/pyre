#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a pipe channel refuses to carry open descriptors, and writes nothing when it does
"""


def test():
    # access the package
    import pyre.ipc

    # make a pair of pipe channels
    parent, child = pyre.ipc.newPipe().open()
    # carefully
    try:
        # ask one of them to carry one of its own descriptors
        parent.write(bytes=b"x", descriptors=[parent.inbound])
    # it refuses
    except pyre.ipc.exceptions.CarriageError as error:
        # naming the channel
        assert error.channel is parent
    # anything else
    else:
        # is a failure
        assert False, "the pipe carried descriptors"
    # make sure nothing was written, so the peer has nothing waiting
    child.setBlocking(False)
    # by attempting to
    try:
        # read
        child.read(minlen=0, maxlen=1)
    # if there is nothing to read
    except BlockingIOError:
        # all is well
        pass
    # anything else
    else:
        # is a failure
        assert False, "the refused write left bytes behind"

    # clean up
    parent.close()
    # both ends
    child.close()

    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
