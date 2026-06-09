#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify the psl selector preserves write interest that a read handler arms on its own fd during its
own dispatch -- the scenario the streaming server relies on, and the one that exposed the stale-mask
bug in {watch}
"""

# externals
import socket

# the framework
import pyre.ipc
from pyre.units.SI import second


# a minimal channel wrapping one end of a socket pair; the dispatcher reads the {inbound}/{outbound}
# endpoints and the handlers use {recv}/{send}
class Channel:
    """
    A socket-backed channel whose two endpoints are the same socket
    """

    # meta-methods
    def __init__(self, sock):
        # the socket both endpoints resolve to
        self.sock = sock
        # all done
        return

    # access to the endpoints
    @property
    def inbound(self):
        """
        The endpoint the dispatcher watches for read-readiness
        """
        # the socket itself
        return self.sock

    @property
    def outbound(self):
        """
        The endpoint the dispatcher watches for write-readiness
        """
        # the socket itself
        return self.sock

    # input/output
    def recv(self, n):
        """
        Consume up to {n} bytes from the socket
        """
        # delegate to the socket
        return self.sock.recv(n)

    def send(self, data):
        """
        Send {data}, returning the number of bytes accepted
        """
        # delegate to the socket
        return self.sock.send(data)


def test():
    # a connected socket pair; we watch one end
    a, b = socket.socketpair()
    # the watched end must be non-blocking so the write handler can probe it safely
    a.setblocking(False)
    # wrap it as a channel
    channel = Channel(a)

    # the selector under test
    selector = pyre.ipc.newPSL(name="pyre.selectors.psl")

    # a record of which handlers ran
    fired = {"read": False, "write": False}

    # the write handler: it only needs to prove that it ran
    def onWrite(channel, **kwds):
        """
        Mark that write-readiness fired and stop the loop
        """
        # note that write-readiness fired
        fired["write"] = True
        # we have what we came for, so end the watch loop promptly
        selector.stop()
        # release the write registration
        return False

    # the read handler: while it runs it arms WRITE interest on the SAME fd -- the case that, before
    # the fix, had its freshly added interest clobbered by a stale pre-dispatch mask snapshot
    def onRead(channel, **kwds):
        """
        Mark that read-readiness fired and arm write interest mid-dispatch
        """
        # note that read-readiness fired
        fired["read"] = True
        # drain the byte so the fd is no longer read-ready
        channel.recv(64)
        # arm write interest on this same fd, right now, inside the read dispatch
        selector.whenWriteReady(channel=channel, call=onWrite)
        # release the read registration
        return False

    # a safety alarm so the loop can never hang if the bug returns and write never fires
    def giveup(timestamp):
        """
        Abandon the watch loop so the test fails cleanly instead of hanging
        """
        # stop watching
        selector.stop()
        # all done
        return

    # watch the read side
    selector.whenReadReady(channel=channel, call=onRead)
    # arm the safety alarm a couple of seconds out
    selector.alarm(interval=2 * second, call=giveup)
    # make the read side ready by sending it a byte
    b.send(b"x")
    # run the loop until the handlers settle, or the safety alarm trips
    selector.watch()

    # the read handler must have run
    assert fired["read"]
    # and the write interest it armed mid-dispatch must have survived to fire
    assert fired["write"]

    # clean up the sockets
    a.close()
    b.close()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
