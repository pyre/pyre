#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that interest registered on a channel while its own pile is being dispatched is
neither invoked prematurely nor lost

The successor's wakeup is delivered only after the current dispatch pass, so a selector that
invokes it early finds an empty channel, and one that drops it never delivers the record
"""

# externals
import select

# access the package
import pyre.ipc

# the unit of time
from pyre.units.SI import second


def test():
    # build a selector
    s = pyre.ipc.newSelector()
    # and a pair of channels
    parent, child = pyre.ipc.newSocket().open()
    # the record of what fired, in order
    log = []

    # the handler that re-arms the same channel while being dispatched
    def first(channel, **kwds):
        """
        Consume the wakeup and register a successor on the same channel and direction
        """
        # drain the byte that woke us
        channel.read(minlen=1, maxlen=1)
        # make a record
        log.append("first")
        # register the successor on the same channel, same direction
        s.whenReadReady(channel=channel, call=successor)
        # deliver its wakeup only after this dispatch pass completes
        s.alarm(interval=0.05 * second, call=wake)
        # this handler is done
        return False

    # the successor
    def successor(channel, **kwds):
        """
        Fire on a later dispatch pass, once the wakeup has been delivered
        """
        # a premature invocation finds nothing to read
        ready, _, _ = select.select([channel], [], [], 0)
        # record it as such
        if not ready:
            # so the final check can tell the story
            log.append("premature")
            # and bail without blocking
            return False
        # otherwise, drain the byte
        channel.read(minlen=1, maxlen=1)
        # make a record
        log.append("second")
        # and wind down
        s.stop()
        # all done
        return False

    # the deferred wakeup
    def wake(timestamp):
        """
        Make the channel readable, one dispatch pass after the successor was registered
        """
        # send the byte
        child.write(bytes=b"2")
        # don't reschedule
        return None

    # the safety net: a lost registration must not hang the test
    def expire(timestamp):
        """
        Give up
        """
        # wind down
        s.stop()
        # and don't reschedule
        return None

    # arm the first handler
    s.whenReadReady(channel=parent, call=first)
    # wake it
    child.write(bytes=b"1")
    # set the safety net
    s.alarm(interval=1 * second, call=expire)
    # spin
    s.watch()

    # the successor must have fired exactly once, on its own pass
    assert log == ["first", "second"], f"broken dispatch: {log}"
    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
