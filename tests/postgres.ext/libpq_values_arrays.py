#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that arrays reach python as lists of their elements
"""


def test():
    """
    Read arrays of integers and of text through the bindings
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # ask for one of each, with the awkward cases among the text: a comma, a quote, a brace,
    # an empty string and a {NULL}
    row = connection.exec(
        """SELECT ARRAY[1, 2, 3]::int8[] AS numbers,"""
        """ ARRAY['a,b', 'say "hi"', '{x}', '', NULL]::text[] AS words"""
    )[0]
    # the numbers
    assert row["numbers"] == [1, 2, 3], repr(row["numbers"])
    # and the words, each exactly as it was
    assert row["words"] == ["a,b", 'say "hi"', "{x}", "", None], repr(row["words"])
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
