#!/usr/bin/env python3
# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 1998-2026 all rights reserved


"""
Verify that an array entry that spells NULL in quotes is the text, not a missing value
"""


def test():
    """
    Read an array that holds both a missing entry and the word NULL
    """
    # access the bindings
    from pyre.extensions import libpq

    # open a session
    connection = libpq.Connection({"dbname": "postgres"})
    # ask for one of each
    value = connection.exec("SELECT ARRAY[NULL, 'NULL', 'back\\slash'] AS words")[0]["words"]
    # the first is missing, the second is the word, and the third keeps its backslash
    assert value == [None, "NULL", "back\\slash"], repr(value)
    # all done
    return


# main
if __name__ == "__main__":
    # run the test
    test()


# end of file
