#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a PSL selector survives descriptor number reuse within a single dispatch cycle

A handler closes its own channel, opens a fresh one that the kernel gives the same descriptor
number, and registers interest with the same event mask; the fresh registration must be live,
not a phantom left behind by stale bookkeeping
"""

# externals
import pyre.ipc

# the unit of time for the safety net
from pyre.units.SI import second


def scenario(transport):
    """
    Run the close-and-reuse scenario over channels built by {transport}
    """
    # build a selector
    s = pyre.ipc.newPSL()
    # and the original pair of channels
    parent, child = transport.open()
    # remember the descriptor number of the watched end
    old = parent.inbound if isinstance(parent.inbound, int) else parent.fileno()
    # the record of what fired
    fired = []
    # and a parking spot for the replacement pair, so it outlives the handler
    replacement = {}

    # the handler that springs the trap
    def killer(channel, **kwds):
        """
        Close the dispatched channel and reincarnate its descriptor number
        """
        # drain the byte that woke us
        channel.read(minlen=1, maxlen=1)
        # close both ends, freeing their descriptor numbers
        parent.close()
        child.close()
        # open a fresh pair; the kernel hands back the lowest free numbers
        p, c = transport.open()
        # park them
        replacement["pair"] = (p, c)
        # find the end that reincarnated the old number
        fresh = p if (p.inbound if isinstance(p.inbound, int) else p.fileno()) == old else c
        other = c if fresh is p else p
        # this scenario is about number reuse; insist it actually happened
        freshfd = fresh.inbound if isinstance(fresh.inbound, int) else fresh.fileno()
        assert freshfd == old
        # register interest with the same mask as the channel just closed
        s.whenReadReady(channel=fresh, call=survivor)
        # and make the fresh channel readable right away
        other.write(bytes=b"x")
        # this handler is done
        return False

    # the handler that must fire despite the reuse
    def survivor(channel, **kwds):
        """
        Prove the fresh registration is live
        """
        # drain the byte
        channel.read(minlen=1, maxlen=1)
        # make a record
        fired.append(True)
        # and wind down
        s.stop()
        # all done
        return False

    # the safety net: a wedged selector must not hang the test
    def expire(timestamp):
        """
        Give up
        """
        # wind down
        s.stop()
        # and don't reschedule
        return None

    # arm the trap
    s.whenReadReady(channel=parent, call=killer)
    # make the original channel readable
    child.write(bytes=b"!")
    # set the safety net
    s.alarm(interval=1 * second, call=expire)
    # spin
    s.watch()

    # the fresh registration must have fired
    assert fired, f"phantom registration: the reused descriptor never fired"
    # all done
    return


def test():
    # the scenario must hold over socket pairs, whose table keys are channel objects
    scenario(transport=pyre.ipc.newSocket())
    # and over pipes, whose table keys are raw descriptor numbers
    scenario(transport=pyre.ipc.newPipe())
    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
