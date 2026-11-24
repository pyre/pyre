#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that a setting of a session given as a truth value reaches libpq as the 1 or 0 it reads
"""


def test():
    """
    Open sessions with keepalives turned on and off as truth values
    """
    # access the bindings
    from pyre.extensions import libpq

    # for each truth value
    for keepalives in (True, False):
        # open a session with it
        connection = libpq.Connection({"dbname": "postgres", "keepalives": keepalives})
        # which is up
        assert connection.ok, keepalives
        # hang up
        connection.close()
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
