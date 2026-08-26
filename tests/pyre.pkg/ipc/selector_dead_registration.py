#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a selector survives a registration whose channel was closed behind its back,
and keeps serving the live ones
"""

# access the package
import pyre.ipc

# the unit of time for the safety net
from pyre.units.SI import second


def scenario(factory):
    """
    Run the dead-registration scenario on a dispatcher built by {factory}
    """
    # build a selector
    s = factory()
    # a pair of channels that will die
    doomedParent, doomedChild = pyre.ipc.newSocket().open()
    # and a pair that stays alive
    parent, child = pyre.ipc.newSocket().open()
    # the record of what fired
    fired = []

    # the handler for the dead channel; it must never fire
    def ghost(channel, **kwds):
        """
        A handler stranded on a dead channel
        """
        # make a record, so the check below can complain
        fired.append("ghost")
        # and don't reschedule
        return False

    # the handler for the live channel
    def live(channel, **kwds):
        """
        Prove the live channel is still served
        """
        # drain the byte
        channel.read(minlen=1, maxlen=1)
        # make a record
        fired.append("live")
        # and wind down
        s.stop()
        # all done
        return False

    # the safety net
    def expire(timestamp):
        """
        Give up
        """
        # wind down
        s.stop()
        # and don't reschedule
        return None

    # register both
    s.whenReadReady(channel=doomedParent, call=ghost)
    s.whenReadReady(channel=parent, call=live)
    # kill the doomed pair behind the selector's back
    doomedParent.close()
    doomedChild.close()
    # make the live channel readable
    child.write(bytes=b"!")
    # set the safety net
    s.alarm(interval=1 * second, call=expire)
    # spin; a fragile selector crashes or wedges here
    s.watch()

    # the live channel was served, and the ghost stayed quiet
    assert fired == ["live"], f"dead registration disrupted service: {fired}"
    # all done
    return


def test():
    # the scenario must hold on the classic selector
    scenario(factory=pyre.ipc.newSelector)
    # and on the psl flavor
    scenario(factory=pyre.ipc.newPSL)
    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
