#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the relay takes a signal over while it has handlers for it, and hands it back,
along with the wakeup descriptor of the interpreter, once the last one is gone; and that a loop
left with nothing to watch but signals has run out of work
"""


def wakeup():
    """
    Peek at the wakeup descriptor of the interpreter, without disturbing it
    """
    # externals
    import signal

    # the only way to read it is to replace it
    current = signal.set_wakeup_fd(-1)
    # so put it back, if there was one
    if current != -1:
        # the way the relay installs it
        signal.set_wakeup_fd(current, warn_on_full_buffer=False)
    # and hand it off
    return current


def test():
    # externals
    import signal

    # support
    import pyre.ipc

    # the relay
    relay = pyre.ipc.signals()

    # a handler the relay must hand the signal back to
    def original(signum, frame):
        # nothing to do
        return

    # install it
    signal.signal(signal.SIGUSR1, original)
    # at first, the relay is in charge of nothing
    assert relay.channel() is None
    assert wakeup() == -1

    # make an event loop
    dispatcher = pyre.ipc.newPSL()

    # a handler for the signal
    def handler(signal, **kwds):
        # that stays registered
        return True

    # relay the signal to it
    dispatcher.whenSignal(signal=signal.SIGUSR1, call=handler)
    # the relay is now in charge of the signal
    assert list(relay.signals()) == [signal.SIGUSR1]
    # it took the signal over
    assert signal.getsignal(signal.SIGUSR1) is not original
    # and installed its end of the socket pair as the wakeup descriptor
    assert wakeup() != -1
    # which the loop watches
    assert relay.channel() in set(dispatcher.channels())

    # with nothing else to watch and no alarms, the loop has run out of work, so it returns
    # right away instead of sleeping until a signal arrives
    dispatcher.watch()

    # let go of the signal
    relay.forget(signal=signal.SIGUSR1, call=handler)
    # the relay is in charge of nothing
    assert list(relay.signals()) == []
    assert relay.channel() is None
    # the signal is back with its original handler
    assert signal.getsignal(signal.SIGUSR1) is original
    # the wakeup descriptor is released
    assert wakeup() == -1
    # and the loop no longer watches the relay
    assert list(dispatcher.channels()) == []

    # a component whose handler is one of its methods
    class listener:
        """
        Something that listens for the signal
        """

        def heard(self, signal, **kwds):
            """
            The handler
            """
            # stay registered
            return True

    # make one
    ear = listener()
    # relay the signal to its method
    dispatcher.whenSignal(signal=signal.SIGUSR1, call=ear.heard)
    # and forget it, through a fresh lookup of the same method
    relay.forget(signal=signal.SIGUSR1, call=ear.heard)
    # which is enough to hand the signal back
    assert list(relay.signals()) == []
    assert signal.getsignal(signal.SIGUSR1) is original

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
