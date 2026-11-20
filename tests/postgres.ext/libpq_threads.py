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

    # make a few threads
    threads = [threading.Thread(target=worker, args=(number,)) for number in range(8)]
    # go through them
    for thread in threads:
        # and start each one
        thread.start()
    # go through them again
    for thread in threads:
        # and wait for each one to finish
        thread.join()
    # none of them should have had trouble
    assert not problems, "\n".join(problems[:10])
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
