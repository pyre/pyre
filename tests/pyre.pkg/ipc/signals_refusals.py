#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the relay refuses what the interpreter does not allow, and leaves things as it
found them: a request from a thread other than the main one, a wakeup descriptor that somebody
else owns, and a signal that cannot be caught
"""


def test():
    # externals
    import signal
    import socket
    import threading

    # support
    import pyre.ipc

    # the relay
    relay = pyre.ipc.signals()
    # make an event loop
    dispatcher = pyre.ipc.newPSL()

    # a handler that is never invoked
    def handler(signal, **kwds):
        # stay registered
        return True

    # the outcome of the request from the thread
    outcome = []

    # ask for a signal from a thread other than the main one
    def ask():
        # carefully
        try:
            # ask
            dispatcher.whenSignal(signal=signal.SIGUSR1, call=handler)
        # it is refused
        except pyre.ipc.exceptions.SignalRelayError as error:
            # record it
            outcome.append(error)
        # all done
        return

    # run it
    thread = threading.Thread(target=ask)
    thread.start()
    thread.join()
    # the request was refused
    assert len(outcome) == 1
    # and the relay is in charge of nothing
    assert relay.channel() is None

    # somebody else takes the wakeup descriptor
    theirs, other = socket.socketpair()
    theirs.setblocking(False)
    signal.set_wakeup_fd(theirs.fileno())
    # carefully
    try:
        # ask for a signal
        dispatcher.whenSignal(signal=signal.SIGUSR1, call=handler)
    # it is refused
    except pyre.ipc.exceptions.SignalRelayError:
        # as it should be
        pass
    # if it isn't
    else:
        # it's a bug
        assert False, "the relay took over a wakeup descriptor it does not own"
    # the descriptor still belongs to its owner
    assert signal.set_wakeup_fd(-1) == theirs.fileno()
    # who is done with it
    theirs.close()
    other.close()
    # and the relay is in charge of nothing
    assert relay.channel() is None

    # ask for a signal that cannot be caught
    try:
        # by anybody
        dispatcher.whenSignal(signal=signal.SIGKILL, call=handler)
    # it is refused
    except pyre.ipc.exceptions.SignalRelayError:
        # as it should be
        pass
    # if it isn't
    else:
        # it's a bug
        assert False, "the relay took over SIGKILL"
    # and the relay let go of the wakeup descriptor it took for it
    assert relay.channel() is None
    assert signal.set_wakeup_fd(-1) == -1

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
