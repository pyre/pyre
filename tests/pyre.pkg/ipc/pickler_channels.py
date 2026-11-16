#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that channels travel whole inside a pickled message over a socket pair: a process that
was forked before the channels existed receives copies of them, and talks through both
"""


def test():
    # externals
    import os

    # access the package
    import pyre.ipc

    # the channel the message travels over
    parent, child = pyre.ipc.newSocket().open()
    # fork
    pid = os.fork()
    # in the parent process
    if pid > 0:
        # release the child's end
        child.close()
        # and invoke the parent behavior
        return onParent(pid=pid, channel=parent)
    # in the child, release the parent's end
    parent.close()
    # and invoke the child behavior
    return onChild(channel=child)


def onParent(pid, channel):
    """
    Make channels the child could not have inherited, send them, and listen on my ends
    """
    # externals
    import os

    # access the package
    import pyre.ipc

    # a pair of pipe channels
    pipes = pyre.ipc.newPipe().open()
    # and a pair of socket channels
    sockets = pyre.ipc.newSocket().open()
    # send the child's ends, inside a message
    pyre.ipc.newPickler().send(
        item={"pipe": pipes.child, "socket": sockets.child, "note": "two channels"},
        channel=channel,
    )
    # my copies of the child's ends are no longer mine to use
    pipes.child.close()
    # both of them
    sockets.child.close()
    # the child writes through its pipe channel
    assert pipes.parent.read(minlen=4, maxlen=4) == b"pipe"
    # and through its socket channel
    assert sockets.parent.read(minlen=6, maxlen=6) == b"socket"
    # wait for it
    _, status = os.waitpid(pid, 0)
    # and make sure it was happy
    assert status == 0
    # clean up
    for end in (pipes.parent, sockets.parent, channel):
        # one channel at a time
        end.close()
    # all done
    return


def onChild(channel):
    """
    Receive the channels and talk through them
    """
    # externals
    import os

    # access the package
    import pyre.ipc

    # get the message
    message = pyre.ipc.newPickler().recv(channel=channel)
    # the plain part made it
    assert message["note"] == "two channels"
    # and the channels arrived as channels of the right kind
    assert type(message["pipe"]).__name__ == "Pipe"
    # both of them
    assert type(message["socket"]).__name__ == "SocketPair"
    # nothing is left over from the trip
    assert channel.arrivals == []
    # talk through the pipe channel
    message["pipe"].write(bytes=b"pipe")
    # and through the socket channel
    message["socket"].write(bytes=b"socket")
    # and leave without going back to the parent's code
    os._exit(0)


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
