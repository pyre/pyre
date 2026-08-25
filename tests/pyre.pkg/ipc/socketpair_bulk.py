#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Push a payload much larger than the socket buffers through a socket pair

This exercises the reassembly loop in the channel {read}: the payload arrives in many packets
and the marshaler must collect them all before unpickling
"""

# a deterministic payload of one megabyte
payload = bytes(range(256)) * (1024 * 4)


def test():
    # externals
    import os

    # access the package
    import pyre.ipc

    # make a pickler
    m = pyre.ipc.newPickler()
    # and a pair of connected channels
    parent, child = pyre.ipc.socketpair()

    # fork
    pid = os.fork()
    # in the parent process
    if pid > 0:
        # invoke the parent behavior
        return onParent(child_pid=pid, marshaler=m, channel=parent)
    # in the child
    return onChild(marshaler=m, channel=child)


def onParent(child_pid, marshaler, channel):
    """Send the bulk payload and verify the echo"""
    # externals
    import os

    # send the payload
    marshaler.send(payload, channel)
    # get the echo
    echo = marshaler.recv(channel)
    # verify it survived the round trip intact
    assert echo == payload
    # harvest the child and verify it exited cleanly
    _, status = os.waitpid(child_pid, 0)
    assert status == 0
    # all done
    return


def onChild(marshaler, channel):
    """Echo whatever arrives back to the sender"""
    # get the payload
    incoming = marshaler.recv(channel)
    # and bounce it back
    marshaler.send(incoming, channel)
    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
