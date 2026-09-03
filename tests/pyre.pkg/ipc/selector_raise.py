#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a handler that raises does not take the rest of its channel's handlers with it

The selector takes possession of a channel's handlers before invoking them, so that interest
registered while they run is not invoked prematurely. A handler that raises unwinds through
that pass; the handlers that never got their turn are still interested, and losing them
leaves a channel nobody listens to, which is a silent failure. So the ones that did not run
keep their place, the one that raised is dropped, and the exception still reaches the caller
"""

# support
import pyre


# the marker of a handler that fails
class Failure(Exception):
    """
    What the failing handler raises
    """


def test():
    # a pair of connected channels
    reader, writer = pyre.ipc.newSocket().open()
    # a selector
    selector = pyre.ipc.newPSL()
    # the record of who ran
    ran = []

    # a handler that raises
    def failing(channel, **kwds):
        """
        Fail, after noting that i ran
        """
        # note
        ran.append("failing")
        # and fail
        raise Failure("the failing handler")

    # a handler that never gets its turn on the first pass
    def patient(channel, **kwds):
        """
        Note that i ran, and ask to stay
        """
        # note
        ran.append("patient")
        # and stay registered
        return True

    # register both, the failing one first
    selector.whenReadReady(channel=reader, call=failing)
    selector.whenReadReady(channel=reader, call=patient)
    # make the channel readable
    writer.write(bytes=b"x")
    # run the loop, which should raise on the first pass
    try:
        # watch
        selector.watch()
    # the failure reaches the caller
    except Failure:
        # as it should
        pass
    # anything else is wrong
    else:
        # so complain
        assert False, "the failing handler did not raise through the loop"
    # only the failing handler got its turn
    assert ran == ["failing"]
    # the patient one kept its place
    registered = [event.handler for event in selector._read[reader.inbound]]
    assert patient in registered
    # and the failing one was dropped
    assert failing not in registered

    # the alarm that winds down the loop once the patient handler has had its turn
    def expire(timestamp):
        """
        Stop the loop
        """
        # stop
        selector.stop()
        # and don't reschedule
        return None

    # let the loop run again; the byte is still there, so the patient handler runs, on every
    # turn of the loop until the alarm stops it, since nobody consumes the byte
    selector.alarm(interval=0.1 * pyre.units.SI.second, call=expire)
    selector.watch()
    # it ran
    assert "patient" in ran
    # the failing one did not run again
    assert ran.count("failing") == 1
    # and, having asked to stay, the patient one is still registered
    assert patient in [event.handler for event in selector._read[reader.inbound]]

    # clean up
    reader.close()
    writer.close()
    # all done
    return selector


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
