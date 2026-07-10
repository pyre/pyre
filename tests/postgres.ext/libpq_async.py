#!/usr/bin/env python3
# -*- Python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Submit a statement for asynchronous processing, collect its results one at a time, and verify
that a failure among them does not derail the collection
"""


def settle(connection):
    """
    Wait for the statement in flight to finish

    This is the loop the asynchronous calls exist to support: read whatever has arrived, ask
    whether the answer is complete, and go around again. The bindings this package replaces threw
    away the answer of {consume}, and so a loop like this one could not tell a socket that had
    gone quiet from one that had gone away
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
    assert answer is not None
    assert answer.ok
    assert answer[0][0] == "42"
    # the second is the sign that the server is done, and the session may be used again
    assert connection.result() is None

    # a statement that fails does not throw its way out of the collection loop; the session must
    # be drained before it may be used again, and a call that threw partway through would leave
    # it mid-answer
    connection.send("SELECT * FROM pyre_no_such_table")
    assert settle(connection)

    # so drain the whole answer, whatever it says
    harvest = []
    while True:
        result = connection.result()
        if result is None:
            break
        harvest.append(result)

    # the server produced exactly one result, which says the statement did not run
    assert len(harvest) == 1
    assert not harvest[0].ok
    # and which, on request, names the condition the server named: the very same classification
    # the synchronous calls make
    try:
        harvest[0].check("SELECT * FROM pyre_no_such_table")
        assert False, "a failed result did not raise when checked"
    except exceptions.ProgrammingError as error:
        assert error.sqlstate == "42P01"

    # the session, having been drained, works again
    assert connection.exec("SELECT 1")[0][0] == "1"

    # a message from another session; there is only one here, and postgres delivers a
    # notification to the session that raised it
    connection.exec("LISTEN pyre_channel")
    connection.exec("NOTIFY pyre_channel, 'the payload'")
    # notifications ride on the back of ordinary traffic, so they must be read off the socket
    connection.consume()

    # collect the one we sent
    message = connection.notification()
    assert message is not None
    assert message.channel == "pyre_channel"
    assert message.payload == "the payload"
    assert message.backend == connection.backend
    # and there are no more
    assert connection.notification() is None

    # all done
    return


# main
if __name__ == "__main__":
    test()


# end of file
