#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a select selector forgets a channel: its handlers never fire, a fresh channel that
recycles its descriptor numbers is watched normally, and a handler that forgets its own channel
while it runs is not put back
"""

# externals
import pyre.ipc

# the unit of time for the safety net
from pyre.units.SI import second


def scenario(transport, factory):
    """
    Run the scenario over channels built by {transport}, watched by a dispatcher from {factory}
    """
    # build a dispatcher
    s = factory()
    # and a pair of channels
    parent, child = transport.open()
    # the record of what fired
    fired = []

    # the safety net: a wedged dispatcher must not hang the test
    def expire(timestamp):
        """
        Give up
        """
        # wind down
        s.stop()
        # and don't reschedule
        return None

    # a handler that must never fire
    def stale(channel, **kwds):
        """
        Fire only if the forgotten channel was not forgotten
        """
        # make a record
        fired.append("stale")
        # and wind down
        s.stop()
        # all done
        return False

    # watch the channel for reading and writing
    s.whenReadReady(channel=parent, call=stale)
    s.whenWriteReady(channel=parent, call=stale)
    # it is watched
    assert parent in set(s.channels())
    # forget it
    s.forget(channel=parent)
    # it is not watched any more
    assert parent not in set(s.channels())
    # close it, freeing its descriptor numbers
    parent.close()
    child.close()

    # a fresh pair, which recycles them
    p, c = transport.open()

    # a handler that must fire
    def live(channel, **kwds):
        """
        Prove the fresh channel is watched
        """
        # drain the byte
        channel.read(minlen=1, maxlen=1)
        # make a record
        fired.append("live")
        # and wind down
        s.stop()
        # all done
        return False

    # watch the fresh channel
    s.whenReadReady(channel=p, call=live)
    # make it readable
    c.write(bytes=b"x")
    # set the safety net
    s.alarm(interval=1 * second, call=expire)
    # spin
    s.watch()
    # only the fresh channel fired
    assert fired == ["live"], fired

    # a handler that forgets its own channel while it runs
    def forgetful(channel, **kwds):
        """
        Forget my channel, and ask to be put back anyway
        """
        # drain the byte
        channel.read(minlen=1, maxlen=1)
        # forget the channel
        s.forget(channel=channel)
        # make a record
        fired.append("forgetful")
        # wind down
        s.stop()
        # and ask to be kept, which must not happen
        return True

    # watch the fresh channel with it
    s.whenReadReady(channel=p, call=forgetful)
    # make it readable
    c.write(bytes=b"y")
    # set the safety net
    s.alarm(interval=1 * second, call=expire)
    # spin
    s.watch()
    # the handler ran
    assert fired[-1] == "forgetful", fired
    # and was not put back
    assert p not in set(s.channels())

    # clean up
    p.close()
    c.close()
    # all done
    return


def test():
    # the scenario must hold over socket pairs, whose table keys are channel objects
    scenario(transport=pyre.ipc.newSocket(), factory=pyre.ipc.newSelector)
    # and over pipes, whose table keys are raw descriptor numbers
    scenario(transport=pyre.ipc.newPipe(), factory=pyre.ipc.newSelector)
    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
