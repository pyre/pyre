#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Grant a child process access to an open file by shipping its descriptor over a socket pair

This is the capability that distinguishes socket pairs from pipes: the descriptor crosses the
process boundary through {SCM_RIGHTS}, not through fork inheritance, so it works for files
opened long after the child was spawned
"""

# what the child writes into the borrowed file
marker = b"delivered by descriptor passing"


def test():
    # externals
    import os

    # access the package
    import pyre.ipc

    # make a pair of connected channels
    parent, child = pyre.ipc.socketpair()

    # fork
    pid = os.fork()
    # in the parent process
    if pid > 0:
        # invoke the parent behavior
        return onParent(child_pid=pid, channel=parent)
    # in the child
    return onChild(channel=child)


def onParent(child_pid, channel):
    """Open a scratch file after the fork and lend its descriptor to the child"""
    # externals
    import os
    import tempfile

    # make a scratch file; the child cannot have inherited it since it does not exist yet
    document = tempfile.TemporaryFile()
    # lend its descriptor to the child
    channel.sendDescriptors(descriptors=[document.fileno()])
    # wait for the child to finish writing and verify it exited cleanly
    _, status = os.waitpid(child_pid, 0)
    assert status == 0
    # rewind the file
    document.seek(0)
    # and verify the child's writes landed in it
    assert document.read() == marker
    # all done
    return


def onChild(channel):
    """Receive the descriptor and write through it"""
    # externals
    import os

    # receive the descriptor and the payload that carried it
    payload, descriptors = channel.recvDescriptors(limit=1)
    # the default payload is a single null byte
    assert payload == b"\x00"
    # exactly one descriptor made the trip
    assert len(descriptors) == 1
    # write the marker through the borrowed descriptor
    os.write(descriptors[0], marker)
    # and return my copy to the kernel; the parent still holds its own
    os.close(descriptors[0])
    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
