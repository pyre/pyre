#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a session collects the notifications another session raises on a channel it listens
to
"""


def test():
    """
    Listen on a channel in one session, notify it from another, and collect the message
    """
    # externals
    import select

    # access the bindings
    from pyre.extensions import libpq

    # open the session that listens
    listener = libpq.Connection({"dbname": "postgres"})
    # on a channel
    listener.exec("LISTEN pyre_notify_other")
    # open the session that notifies
    notifier = libpq.Connection({"dbname": "postgres"})
    # and raise a notification on the channel
    notifier.exec("NOTIFY pyre_notify_other, 'from the other side'")

    # wait for the message to reach the listener, for five seconds at most
    ready, _, _ = select.select([listener.socket], [], [], 5)
    # it arrived
    assert ready, "no notification arrived"
    # read it off the socket
    listener.consume()
    # and collect it
    message = listener.notification()
    # it is there
    assert message is not None
    # on the channel
    assert message.channel == "pyre_notify_other", message.channel
    # carrying what was sent
    assert message.payload == "from the other side", message.payload
    # from the other session
    assert message.backend == notifier.backend, (message.backend, notifier.backend)
    # and there are no more
    assert listener.notification() is None
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
