#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that another thread can ask the server to give up on the statement a session is running
"""


def test():
    """
    Run a statement that sleeps for ten seconds, and cancel it from another thread
    """
    # externals
    import threading
    import time

    # access the package
    import pyre.db

    # and the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})

    # the thread that cancels
    def cancel():
        """
        Give the statement time to reach the server, then ask the server to give up on it
        """
        # wait a little
        time.sleep(0.5)
        # and cancel
        connection.cancel()
        # all done
        return

    # make the thread
    canceller = threading.Thread(target=cancel)
    # and start it
    canceller.start()
    # note the time
    start = time.monotonic()
    # carefully
    try:
        # run a statement that would take ten seconds
        connection.exec("SELECT pg_sleep(10)")
    # the failure
    except pyre.db.exceptions.OperationalError as error:
        # names the cancellation
        assert error.sqlstate == "57014", error.sqlstate
    # a statement that ran to the end
    else:
        # was never cancelled
        assert False, "the statement ran to the end"
    # wait for the other thread
    canceller.join()

    # the statement stopped well before it would have finished
    assert time.monotonic() - start < 5, time.monotonic() - start
    # and the session is usable
    assert connection.exec("SELECT 1")[0][0] == 1
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
