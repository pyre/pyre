#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that dates before the common era, which python cannot hold, are refused
"""


def test():
    """
    Read a date before the common era through the bindings
    """
    # access the bindings
    from pyre.extensions import libpq

    # and the exceptions the package raises
    from pyre.db import exceptions

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # ask for the ides of march
    row = connection.exec("SELECT date '0044-03-15 BC' AS ides")[0]
    # the value
    try:
        # must not reach python
        value = row["ides"]
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
