#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the end of a day, which postgres writes as 24:00:00 and python cannot hold, is
refused rather than read as the start of one
"""


def test():
    """
    Read the time at the end of a day through the bindings
    """
    # access the bindings
    from pyre.extensions import libpq

    # and the exceptions the package raises
    from pyre.db import exceptions

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # ask for the end of the day
    row = connection.exec("SELECT time '24:00:00' AS end")[0]
    # the value
    try:
        # must not reach python
        value = row["end"]
    # as a data error
    except exceptions.DataError:
        # which is the whole point
        pass
    # and anything else
    else:
        # is a failure
        assert False, repr(value)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
