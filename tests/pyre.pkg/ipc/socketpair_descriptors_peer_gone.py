#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a message that leaves whole with its descriptors is delivered, even when the peer
hangs up right after it arrives
"""


def test():
    # externals
    import os

    # the channel under test
    from pyre.ipc.SocketPair import SocketPair

    # a socket pair whose peer hangs up whenever more bytes are about to follow a message
    class Hangup(SocketPair):
        """
        A channel whose peer leaves before anything after the first send reaches it
        """

        # the end that hangs up
        peer = None

        def sendall(self, data, flags=0):
            """
            Hang up the peer, then send {data}
            """
            # the peer leaves
            self.peer.close()
            # before the bytes go out
            return super().sendall(data, flags)

    # make the channels
    ends = Hangup.open()
    # tell the sending end about its peer
    ends.parent.peer = ends.child
    # make a descriptor to carry
    reader, writer = os.pipe()
    # send a short message along with it, which the socket takes at once
    sent = ends.parent.write(bytes=b"message", descriptors=[reader])
    # and make sure all of it left
    assert sent == len(b"message")
    # clean up
    for descriptor in (reader, writer):
        # one descriptor at a time
        os.close(descriptor)
    # along with my end
    ends.parent.close()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
