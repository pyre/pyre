#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that collecting a copy in that was never ended lets the other threads run while the server
works through the rows it was sent before it hears the copy is abandoned
"""


def test():
    """
    Abandon a copy whose rows take a second to load, while another thread counts
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
        " AS $$ BEGIN PERFORM pg_sleep(0.01); RETURN NEW; END $$"
    )
    # which runs for every row that arrives
    connection.exec(
        "CREATE TRIGGER pyre_slow BEFORE INSERT ON pyre_slow"
        " FOR EACH ROW EXECUTE FUNCTION pg_temp.pyre_slow()"
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

    # start a copy
    copy = connection.copyIn("COPY pyre_slow FROM STDIN")
    # send it a hundred rows, which take a hundredth of a second each to load
    copy.put("".join(f"{row}\n" for row in range(100)))
    # make the watcher
    watcher = threading.Thread(target=watch)
    # and start it
    watcher.start()
    # note the time
    start = time.monotonic()
    # let go of the copy, which abandons it and waits for the server to say it has
    del copy
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
