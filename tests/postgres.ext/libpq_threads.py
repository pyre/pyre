#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that threads sharing one session take turns, so each gets the answer to its own statement
"""


def test():
    """
    Run statements from several threads at once through the same session
    """
    # support
    import threading
    import time

    # access the bindings
    from pyre.extensions import libpq

    # and the exceptions the package raises
    from pyre.db import exceptions

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # the answers each thread got, and the problems
    problems = []

    # each thread asks for its own number, many times over, slowly enough to overlap the others
    def worker(number):
        """
        Ask for {number} back from the server, many times over
        """
        # many times
        for _ in range(50):
            # carefully
            try:
                # ask for my number back, after a pause on the server
                answer = connection.execute("SELECT $1::int AS n, pg_sleep(0.001)", number)
                # read it
                value = int(answer[0]["n"])
                # and if it is not mine
                if value != number:
                    # make a note
                    problems.append(f"thread {number} got {value}")
            # any complaint from the session
            except exceptions.FrameworkError as error:
                # counts
                problems.append(f"thread {number}: {error}")
        # all done
        return

    # make a few threads, which must not keep the interpreter alive if they get stuck
    threads = [threading.Thread(target=worker, args=(number,), daemon=True) for number in range(8)]
    # go through them
    for thread in threads:
        # and start each one
        thread.start()
    # the statements take about a second even one at a time, so give them far longer
    deadline = time.monotonic() + 30
    # go through the threads again
    for thread in threads:
        # and wait for each one to finish, until the deadline
        thread.join(timeout=max(0, deadline - time.monotonic()))
    # the threads still running are stuck waiting for an answer
    stuck = [thread.name for thread in threads if thread.is_alive()]
    # none of them should be
    assert not stuck, f"stuck waiting for the server: {', '.join(stuck)}"
    # and none of them should have had trouble
    assert not problems, "\n".join(problems[:10])
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
