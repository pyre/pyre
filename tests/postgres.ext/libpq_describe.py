#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Check that the description of a prepared statement names the types of its parameters and of the
columns of its rows
"""


def test():
    """
    Prepare a sum of two numbers of different widths, and read its description
    """
    # access the bindings
    from pyre.extensions import libpq

    # the identifier postgres catalogs its wide integers under
    int8 = 20
    # and its narrow ones
    int4 = 23

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # teach it a sum of two numbers of different widths
    connection.prepare("pyre_sum", "SELECT $1::int8 + $2::int4 AS total")
    # and ask what it learned
    description = connection.describe("pyre_sum")
    # the statement takes two parameters
    assert description.parameters == 2, description.parameters
    # a wide one, followed by a narrow one
    assert description.parameterTypes == (int8, int4), description.parameterTypes
    # its rows have one column, with the label it was given
    assert description.headers == ("total",), description.headers
    # and the wider of the two types
    assert description.types == (int8,), description.types
    # and a description carries no rows
    assert len(description) == 0, len(description)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
