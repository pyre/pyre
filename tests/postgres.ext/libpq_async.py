#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


def settle(connection):
    """
    Wait for the statement in flight to finish

    This is the loop the asynchronous calls exist to support: read whatever has arrived, ask
    whether the answer is complete, and go around again. {consume} raises when the socket has
    gone away, so the loop can tell a socket that went quiet from one that died
    """
    # a real client waits on the socket; a test may spin, so long as it gives up eventually
    for _ in range(100_000_000):
        # pull whatever the server has sent into libpq's buffer; a socket that died raises
        connection.consume()
        # and if the answer is complete
        if not connection.busy:
            # we are done waiting
            return True
    # the server never answered
    return False


def test():
    """
    Submit a statement for asynchronous processing, collect its results one at a time, and
    verify that a failure among them does not derail the collection
    """
    # access the bindings
    from pyre.extensions import libpq

    # and the exceptions the package raises
    from pyre.db import exceptions

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})

    # send a statement off without waiting for it
    connection.send("SELECT 42")
    # wait for the server to finish with it
    assert settle(connection)

    # the first result is the answer
    answer = connection.result()
    # it is there
    assert answer is not None
    # the statement ran
    assert answer.ok
    # and produced what was asked for
    assert answer[0][0] == 42
    # the second is the sign that the server is done, and the session may be used again
    assert connection.result() is None

    # a statement that fails does not throw its way out of the collection loop; the session must
    # be drained before it may be used again, and a call that threw partway through would leave
    # it mid-answer
    connection.send("SELECT * FROM pyre_no_such_table")
    # wait for the server to finish with it
    assert settle(connection)

    # so drain the whole answer, whatever it says
    harvest = []
    # one result at a time
    while True:
        # get one
        result = connection.result()
        # if there are no more
        if result is None:
            # the answer is drained
            break
        # otherwise, keep it
        harvest.append(result)

    # the server produced exactly one result
    assert len(harvest) == 1
    # which says the statement did not run
    assert not harvest[0].ok
    # and which, on request, names the condition the server named: the very same classification
    # the synchronous calls make
    try:
        # ask for it
        harvest[0].check("SELECT * FROM pyre_no_such_table")
        # and complain if the result kept quiet
        assert False, "a failed result did not raise when checked"
    # the classification
    except exceptions.ProgrammingError as error:
        # names a missing table
        assert error.sqlstate == "42P01"

    # the session, having been drained, works again
    assert connection.exec("SELECT 1")[0][0] == 1

    # a message from another session; there is only one here, and postgres delivers a
    # notification to the session that raised it, so listen
    connection.exec("LISTEN pyre_channel")
    # and raise one
    connection.exec("NOTIFY pyre_channel, 'the payload'")
    # notifications ride on the back of ordinary traffic, so they must be read off the socket
    connection.consume()

    # collect the one we sent
    message = connection.notification()
    # it is there
    assert message is not None
    # on the channel we listen to
    assert message.channel == "pyre_channel"
    # carrying what we sent
    assert message.payload == "the payload"
    # from this very session
    assert message.backend == connection.backend
    # and there are no more
    assert connection.notification() is None

    # all done
    return


# main
if __name__ == "__main__":
    # do...
    test()


# end of file
