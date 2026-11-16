#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that an idle node stops as soon as it receives {TERM}: it watches a channel that never
speaks and has no alarm to wake it up, so the request reaches it only through the relay
"""


def test():
    # externals
    import os
    import signal
    import time

    # support
    import pyre
    from pyre.nexus.Node import Node
    from pyre.units.SI import second

    # a channel that never speaks, so the node has something to watch and nothing to do
    quiet, mute = pyre.ipc.newSocket().open()

    # a node that keeps track of how it stopped
    class node(Node):
        """
        A node that remembers whether {TERM} stopped it
        """

        @pyre.export
        def stop(self):
            """
            Record the request and stop
            """
            # mark it
            self.stopped = True
            # and chain up
            return super().stop()

        def speak(self, channel, **kwds):
            """
            The handler of the quiet channel, which never runs
            """
            # stay registered
            return True

        def giveUp(self, timestamp):
            """
            The last resort: if {TERM} is not relayed, the node sleeps until this rings
            """
            # mark it
            self.timedOut = True
            # stop the loop
            self.dispatcher.stop()
            # and don't ring again
            return None

        def __init__(self, **kwds):
            # chain up
            super().__init__(**kwds)
            # nothing has happened yet
            self.stopped = False
            self.timedOut = False
            # watch the quiet channel
            self.dispatcher.whenReadReady(channel=quiet, call=self.speak)
            # and arm the last resort well past the signal
            self.dispatcher.alarm(interval=10 * second, call=self.giveUp)
            # all done
            return

    # make a node
    server = node(name="server")
    # get my pid
    pid = os.getpid()
    # fork a child to send the signal
    child = os.fork()
    # in the child
    if child == 0:
        # give the parent time to fall asleep
        time.sleep(0.2)
        # ask it to terminate
        os.kill(pid, signal.SIGTERM)
        # and leave without running the cleanup of the parent
        os._exit(0)

    # in the parent, start the clock
    start = time.monotonic()
    # enter the event loop
    server.dispatcher.watch()
    # stop the clock
    elapsed = time.monotonic() - start
    # collect the child
    os.waitpid(child, 0)
    # {TERM} stopped the node
    assert server.stopped
    # the last resort never rang
    assert not server.timedOut
    # and the node stopped right away, not when the last resort was due
    assert elapsed < 5, elapsed

    # clean up
    quiet.close()
    mute.close()
    # all done
    return server


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
