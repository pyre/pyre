#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that a forked child starts without the relay of its parent: its signals have the
dispositions they had before the relay took them over, and the wakeup descriptor is free, so a
signal sent to the child can neither wake the parent nor run the parent's handlers
"""


def test():
    # externals
    import os
    import signal

    # support
    import pyre.ipc

    # the relay
    relay = pyre.ipc.signals()
    # make an event loop
    dispatcher = pyre.ipc.newPSL()

    # the handler of the signal, which must run only in the parent
    def handler(signal, **kwds):
        # stay registered
        return True

    # relay the signal
    dispatcher.whenSignal(signal=signal.SIGUSR2, call=handler)

    # fork
    pid = os.fork()
    # in the child
    if pid == 0:
        # assume the worst
        status = 1
        # carefully, so that the child leaves no matter what
        try:
            # the relay is in charge of nothing
            assert relay.channel() is None
            assert list(relay.signals()) == []
            # the signal is back to its default disposition
            assert signal.getsignal(signal.SIGUSR2) is signal.SIG_DFL
            # and the wakeup descriptor is free
            assert signal.set_wakeup_fd(-1) == -1
            # all good
            status = 0
        # whatever happened
        finally:
            # leave without running the cleanup of the parent
            os._exit(status)

    # in the parent, wait for the child
    _, status = os.waitpid(pid, 0)
    # it found everything in order
    assert os.waitstatus_to_exitcode(status) == 0
    # while the parent still relays the signal
    assert list(relay.signals()) == [signal.SIGUSR2]
    assert relay.channel() is not None

    # let go of the signal
    relay.forget(signal=signal.SIGUSR2)
    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
