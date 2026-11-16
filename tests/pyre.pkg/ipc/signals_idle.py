#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a signal reaches an idle event loop as soon as it arrives: the loop watches a
channel that never speaks and has no alarm to wake it up, so only the relay can
"""


def check(dispatcher):
    """
    Relay a signal to {dispatcher} while it sleeps, and check its handler stopped the loop
    """
    # externals
    import signal
    import time

    # support
    import pyre.ipc
    from pyre.units.SI import second

    # a channel that never speaks, so the loop has something to watch and nothing to do
    quiet, mute = pyre.ipc.newSocket().open()
    # the signals the handler saw
    seen = []

    # the handler of the signal
    def stop(signal, **kwds):
        # record it
        seen.append(signal)
        # stop the loop
        dispatcher.stop()
        # and stay registered
        return True

    # the handler of the quiet channel, which never runs
    def speak(channel, **kwds):
        # stay registered
        return True

    # the last resort: if the signal is not relayed, the loop sleeps until this rings
    def giveUp(timestamp):
        # mark it
        seen.append("timeout")
        # stop the loop
        dispatcher.stop()
        # and don't ring again
        return None

    # watch the quiet channel
    dispatcher.whenReadReady(channel=quiet, call=speak)
    # ask for the signal
    dispatcher.whenSignal(signal=signal.SIGALRM, call=stop)
    # arm the last resort well past the signal
    dispatcher.alarm(interval=10 * second, call=giveUp)
    # have the kernel send the signal shortly, while the loop sleeps
    signal.setitimer(signal.ITIMER_REAL, 0.1)
    # start the clock
    start = time.monotonic()
    # enter the loop
    dispatcher.watch()
    # stop the clock
    elapsed = time.monotonic() - start
    # the handler saw the signal, exactly once, and the last resort never rang
    assert seen == [signal.SIGALRM], seen
    # and the loop woke up right away, not when the last resort was due
    assert elapsed < 5, elapsed
    # let go of the signal
    pyre.ipc.signals().forget(signal=signal.SIGALRM)
    # and the channel
    dispatcher.forget(channel=quiet)
    quiet.close()
    mute.close()
    # all done
    return


def test():
    # support
    import pyre.ipc

    # check the selector built on {select}
    check(dispatcher=pyre.ipc.newSelector())
    # and the one built on the {selectors} module of the standard library
    check(dispatcher=pyre.ipc.newPSL())
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
