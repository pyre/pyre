#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that the infinite dates and moments of postgres, which python cannot hold, are refused
"""


def test():
    """
    Read an infinite date and an infinite moment through the bindings
    """
    # access the bindings
    from pyre.extensions import libpq

    # and the exceptions the package raises
    from pyre.db import exceptions

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # each of these
    for statement in (
        "SELECT 'infinity'::date AS never",
        "SELECT '-infinity'::timestamptz AS never",
    ):
        # gets the row
        row = connection.exec(statement)[0]
        # but its value
        try:
            # must not reach python
            value = row["never"]
        # as a data error
        except exceptions.DataError as error:
            # that names the column
            assert "never" in str(error), str(error)
        # and anything else
        else:
            # is a failure
            assert False, f"{statement}: {value!r}"
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
