#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that collecting a transaction that is still open lets the other threads run while it waits
for its turn on the session to roll back
"""


def test():
    """
    Abandon a transaction while another thread keeps the session busy for a second, while a third
    counts
    """
    # externals
    import threading
    import time

    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})

    # the moments the watcher woke up at
    moments = []
    # and the signal that stops it
    done = threading.Event()

    # the watcher
    def watch():
        """
        Wake up every hundredth of a second, and note when, until told to stop
        """
        # until told to stop
        while not done.is_set():
            # note the moment
            moments.append(time.monotonic())
            # and sleep, which needs the interpreter to wake up again
            time.sleep(0.01)
        # all done
        return

    # the thread that keeps the session busy
    def work():
        """
        Run a statement that takes a second
        """
        # run it
        connection.exec("SELECT pg_sleep(1)")
        # all done
        return

    # open a transaction, outside any block, so that only its collection ends it
    transaction = libpq.Transaction(connection)
    # make the worker
    worker = threading.Thread(target=work)
    # start it
    worker.start()
    # and give its statement time to reach the server
    time.sleep(0.1)
    # make the watcher
    watcher = threading.Thread(target=watch)
    # and start it
    watcher.start()
    # note the time
    start = time.monotonic()
    # let go of the transaction, which waits for the session before it rolls back
    del transaction
    # the time the collection was over
    end = time.monotonic()
    # tell the watcher to stop
    done.set()
    # and wait for it
    watcher.join()
    # and for the worker
    worker.join()

    # the collection waited for the session
    assert end - start >= 0.4, end - start
    # the moments the watcher woke up at, well inside the wait
    awake = [moment for moment in moments if start + 0.1 < moment < end - 0.1]
    # show that it ran while the session was busy
    assert awake, (start, end, moments)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
