#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that collecting a stream that still has rows to read lets the other threads run while it
reads them
"""


def test():
    """
    Abandon a stream whose rows take a second to make, while another thread counts
    """
    # externals
    import threading
    import time

    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})

    # the moments the other thread woke up at
    moments = []
    # and the signal that stops it
    done = threading.Event()

    # the other thread
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

    # in a transaction block, where an abandoned stream reads its rows to the end
    with libpq.Transaction(connection):
        # a selection whose rows take a hundredth of a second each, and are big enough to fill
        # the buffer the server sends from every few rows, so they arrive as they are made
        stream = connection.stream(
            "SELECT pg_sleep(0.01), repeat('x', 1000) FROM generate_series(1, 100)", batch=1
        )
        # read the first batch
        next(stream)
        # make the watcher
        watcher = threading.Thread(target=watch)
        # and start it
        watcher.start()
        # note the time
        start = time.monotonic()
        # let go of the stream, which reads the rest of the rows as it goes
        del stream
        # the time the collection was over
        end = time.monotonic()
    # tell the watcher to stop
    done.set()
    # and wait for it
    watcher.join()

    # the collection waited for the server
    assert end - start >= 0.4, end - start
    # the moments the other thread woke up at, well inside the wait
    awake = [moment for moment in moments if start + 0.1 < moment < end - 0.1]
    # show that it ran while the server worked
    assert awake, (start, end, moments)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
