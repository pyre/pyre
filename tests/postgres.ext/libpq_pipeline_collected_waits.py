#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that collecting a pipeline whose answers were not read lets the other threads run while it
waits for them
"""


def test():
    """
    Abandon a pipeline whose statement takes a second, while another thread counts
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

    # start a pipeline
    pipeline = connection.pipeline()
    # send it a statement that takes a second
    pipeline.execute("SELECT pg_sleep(1)")
    # make the watcher
    watcher = threading.Thread(target=watch)
    # and start it
    watcher.start()
    # note the time
    start = time.monotonic()
    # let go of the pipeline, which syncs and reads the answer
    del pipeline
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
