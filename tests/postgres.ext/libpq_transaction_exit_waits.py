#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the end of a transaction block lets the other threads run while it waits for the
server to commit
"""


def test():
    """
    Commit a transaction whose commit the server takes half a second over, while another thread
    counts
    """
    # externals
    import threading
    import time

    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # make a table of our own, which goes away with the session
    connection.exec("CREATE TEMPORARY TABLE pyre_slow (id integer)")
    # a function that takes its time
    connection.exec(
        "CREATE FUNCTION pg_temp.pyre_slow() RETURNS trigger LANGUAGE plpgsql"
        " AS $$ BEGIN PERFORM pg_sleep(0.5); RETURN NULL; END $$"
    )
    # which runs when a transaction that added a row commits
    connection.exec(
        "CREATE CONSTRAINT TRIGGER pyre_slow AFTER INSERT ON pyre_slow"
        " DEFERRABLE INITIALLY DEFERRED FOR EACH ROW EXECUTE FUNCTION pg_temp.pyre_slow()"
    )

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

    # in a transaction block
    with libpq.Transaction(connection):
        # add a row, which makes the commit slow
        connection.exec("INSERT INTO pyre_slow VALUES (1)")
        # make the watcher
        watcher = threading.Thread(target=watch)
        # and start it
        watcher.start()
        # note the time as the block ends
        start = time.monotonic()
    # the time the end of the block was over
    end = time.monotonic()
    # tell the watcher to stop
    done.set()
    # and wait for it
    watcher.join()

    # the commit waited for the server
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
